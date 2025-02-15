import os
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import pytz
import dateparser
from docx import Document
from PyPDF2 import PdfReader
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from msal import PublicClientApplication
import requests

# Configuration
CONFIG = {
    "ms_client_id": "YOUR_MICROSOFT_CLIENT_ID",
    "google_credentials": "token.json",
    "timezone": "America/New_York"
}

# Initialize logging
logging.basicConfig(filename='calendar_sync.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentProcessor:
    @staticmethod
    def parse_docx(content: bytes) -> str:
        """Extract text from Word documents"""
        doc = Document(io.BytesIO(content))
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def parse_pdf(content: bytes) -> str:
        """Extract text from PDF documents"""
        reader = PdfReader(io.BytesIO(content))
        return "\n".join([page.extract_text() for page in reader.pages])

    @staticmethod
    def parse_text(content: bytes) -> str:
        """Handle plain text content"""
        return content.decode('utf-8')

class MeetingExtractor:
    def __init__(self, timezone: str = "UTC"):
        self.timezone = pytz.timezone(timezone)
        self.patterns = {
            'datetime': r'\b(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [AP]M)\b',
            'duration': r'Duration:.*?(\d+)\s*minutes?',
            'attendees': r'Attendees:\s*(.*)',
            'location': r'Location:\s*(.*)'
        }

    def extract_info(self, text: str) -> Dict:
        """Extract meeting information using regex patterns"""
        extracted = {
            'title': self._extract_title(text),
            'start': self._extract_datetime(text),
            'duration': self._extract_duration(text),
            'attendees': self._extract_attendees(text),
            'location': self._extract_location(text),
            'description': self._extract_description(text)
        }
        return self._process_results(extracted)

    def _extract_title(self, text: str) -> str:
        return re.search(r'Meeting Title:\s*(.*)', text).group(1) or "Untitled Meeting"

    def _extract_datetime(self, text: str) -> datetime:
        match = re.search(self.patterns['datetime'], text)
        return dateparser.parse(match.group(1), settings={'TIMEZONE': self.timezone.zone})

    # Additional extraction methods for other fields...

class CalendarIntegration:
    def __init__(self):
        self.google_service = self._init_google_calendar()
        self.ms_graph_headers = self._init_microsoft_graph()

    def _init_google_calendar(self):
        creds = Credentials.from_authorized_user_file(CONFIG['google_credentials'], 
                    ['https://www.googleapis.com/auth/calendar'])
        return build('calendar', 'v3', credentials=creds)

    def _init_microsoft_graph(self):
        app = PublicClientApplication(CONFIG['ms_client_id'],
                                    authority="https://login.microsoftonline.com/common")
        result = app.acquire_token_interactive(scopes=["Files.Read.All"])
        return {'Authorization': f'Bearer {result["access_token"]}'}

    def search_document(self):
        """Search for document with pagination handling"""
        items = []
        url = "https://graph.microsoft.com/v1.0/me/drive/root/search(q='work agenda')"
        while url:
            response = requests.get(url, headers=self.ms_graph_headers)
            if response.status_code == 200:
                data = response.json()
                items.extend(data.get('value', []))
                url = data.get('@odata.nextLink')
            else:
                logging.error(f"Search failed: {response.text}")
                break
        return next((item for item in items if item['name'].lower() == 'work agenda'), None)

    def create_calendar_event(self, event_details: Dict):
        """Create event with recurrence handling"""
        try:
            event = self.google_service.events().insert(
                calendarId='primary',
                body=event_details
            ).execute()
            logging.info(f"Event created: {event.get('htmlLink')}")
            return event
        except Exception as e:
            logging.error(f"Event creation failed: {str(e)}")
            raise

def main():
    integrator = CalendarIntegration()
    
    # Search for document
    doc_item = integrator.search_document()
    if not doc_item:
        logging.error("Document not found")
        return

    # Retrieve and parse document
    content = requests.get(doc_item['@microsoft.graph.downloadUrl']).content
    file_ext = os.path.splitext(doc_item['name'])[1].lower()
    
    parser = DocumentProcessor()
    if file_ext == '.docx':
        text = parser.parse_docx(content)
    elif file_ext == '.pdf':
        text = parser.parse_pdf(content)
    else:  # Assume text
        text = parser.parse_text(content)

    # Extract meeting information
    extractor = MeetingExtractor(timezone=CONFIG['timezone'])
    meeting_data = extractor.extract_info(text)
    
    # Create calendar event
    event_body = {
        'summary': meeting_data['title'],
        'location': meeting_data['location'],
        'description': meeting_data['description'],
        'start': {
            'dateTime': meeting_data['start'].isoformat(),
            'timeZone': CONFIG['timezone']
        },
        'end': {
            'dateTime': (meeting_data['start'] + 
                         timedelta(minutes=meeting_data['duration'])).isoformat(),
            'timeZone': CONFIG['timezone']
        },
        'attendees': [{'email': email.strip()} for email in meeting_data['attendees'].split(',')]
    }
    
    # Handle recurrence
    if 'weekly' in text.lower():
        event_body['recurrence'] = ['RRULE:FREQ=WEEKLY;INTERVAL=1']
    
    integrator.create_calendar_event(event_body)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Critical failure: {str(e)}", exc_info=True)