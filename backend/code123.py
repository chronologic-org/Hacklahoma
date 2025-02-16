import os
import logging
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI
from typing import Optional

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HomeworkHelper:
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.auth = None
        self.service = None
        self._authenticate()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _authenticate(self) -> None:
        """Authenticate with Google using OAuth 2.0."""
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.auth = pickle.load(token)
            if not self.auth or not self.auth.valid:
                if self.auth and self.auth.expired and self.auth.refresh_token:
                    self.auth.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path,
                        scopes=['https://www.googleapis.com/auth/documents.readonly']
                    )
                    self.auth = flow.run_local_server(port=0)
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.auth, token)
            self.service = googleapiclient.discovery.build(
                'docs', 'v1', credentials=self.auth)
            logging.info("Successfully authenticated with Google.")
        except googleapiclient.errors.HttpError as e:
            logging.error(f"Google API authentication error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected authentication error: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_document(self, document_id: str) -> str:
        """Retrieve the content of a Google Doc."""
        try:
            document = self.service.documents().get(
                documentId=document_id).execute()
            text = document.get('body', {}).get('content', '')
            return text
        except googleapiclient.errors.HttpError as e:
            logging.error(f"Error fetching document: {str(e)}")
            raise

    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess the text."""
        try:
            # Remove extra whitespace
            text = ' '.join(text.split())
            # Remove headers/footers/comments (example regex)
            text = text.replace("Header:", "").replace("Footer:", "").replace("Comment:", "")
            return text.strip()
        except Exception as e:
            logging.error(f"Error preprocessing text: {str(e)}")
            raise

def query_chatgpt(api_key: str, prompt: str) -> Optional[str]:
    """Query ChatGPT with the given prompt."""
    try:
        openai = OpenAI(api_key=api_key)
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        if response and response.choices:
            return response.choices[0].message['content']
        return None
    except Exception as e:
        logging.error(f"Error querying ChatGPT: {str(e)}")
        return None

def main():
    try:
        # Example usage
        helper = HomeworkHelper("credentials.json")
        document_id = "your_document_id"
        text = helper.get_document(document_id)
        cleaned_text = helper.preprocess_text(text)
        response = query_chatgpt("your_openai_api_key", cleaned_text)
        print(response)
    except Exception as e:
        logging.error(f"Main function error: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
