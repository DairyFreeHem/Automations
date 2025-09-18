import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_apis import data

class Google:
    def __init__(self):
        """
            Initialize Google Authentication
        """
        self.creds = None
        
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        try:
                
            if os.path.exists(data.token_path):
                self.creds = Credentials.from_authorized_user_file(data.token_path, data.SCOPES)
        except:
            print("Could not get token.json file")
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    data.credentials_path, data.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(data.token_path, "w") as token:
                token.write(self.creds.to_json())
