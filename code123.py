import os
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from email.parser import BytesParser
from email.message import Message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_last_email(gmail_service):
    """
    Retrieves the user's last email using the Gmail API.
    """
    try:
        # Get the last message
        messages_response = gmail_service.users().messages().list(
            userId='me',
            maxResults=1
        ).execute()
        
        if not messages_response.get('messages', []):
            logger.error("No messages found.")
            return None
        
        message_id = messages_response['messages'][0]['id']
        
        # Get the message details
        message_response = gmail_service.users().messages().get(
            userId='me',
            id=message_id,
            format='metadata'
        ).execute()
        
        return message_response
        
    except HttpError as error:
        logger.error(f"Gmail API error: {error}")
        return None

def parse_email(message_response):
    """
    Parses the email message to extract relevant information.
    """
    try:
        raw_message = message_response.get('raw', None)
        if not raw_message:
            logger.error("No raw message found.")
            return None
            
        # Convert bytes to string
        raw_bytes = bytes(raw_message, 'utf-8')
        parser = BytesParser()
        email_message = parser.parsebytes(raw_bytes)
        
        subject = email_message['Subject']
        body = ''
        
        # Extract body text
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        return {
            'subject': subject,
            'body': body
        }
        
    except Exception as e:
        logger.error(f"Error parsing email: {e}")
        return None

def create_calendar_event(calendar_service, event_data):
    """
    Creates a new calendar event using the provided data.
    """
    try:
        event = {
            'summary': event_data['subject'],
            'description': event_data['body'],
            'start': {'dateTime': '2023-10-20T09:00:00'},
            'end': {'dateTime': '2023-10-20T10:00:00'}
        }
        
        response = calendar_service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        logger.info(f"Event created: {response.get('id')}")
        return response
        
    except HttpError as error:
        logger.error(f"Calendar API error: {error}")
        return None

def main():
    # Configure credentials
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/calendar.events']
    
    SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_SERVICE_ACCOUNT_KEY', 'service_account_key.json')
    
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    
    # Build Gmail and Calendar services
    gmail_service = build('gmail', 'v1', credentials=credentials)
    calendar_service = build('calendar', 'v3', credentials=credentials)
    
    # Get last email
    last_email = get_last_email(gmail_service)
    if not last_email:
        logger.error("Failed to retrieve last email.")
        return
        
    # Parse email data
    email_data = parse_email(last_email)
    if not email_data:
        logger.error("Failed to parse email.")
        return
        
    # Create calendar event
    create_calendar_event(calendar_service, email_data)
    
if __name__ == "__main__":
    main()
