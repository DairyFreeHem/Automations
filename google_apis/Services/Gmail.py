
import json
from google_apis.Google import Google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Gmail(Google):

    def __init__(self):
        super().__init__()

    def callApi(self,userId):
        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=self.creds)
            return service
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f"An error occurred: {error}")
        
        return None

    def getLabels(self, userId):
        service = self.callApi(userId)
        if not None:
            results = service.users().labels().list(userId=userId).execute()
            labels = results.get("labels", [])
        return []

    def getMails(self,userId:str, query:str, getFullMessage:bool = False, next_page_token:str = None):
        r'''
        Get all emails according to a query
        
        PARAMETERS:
            userId:str - Mail of affected user.
            query:str - Google query to filter by.
            getFullMessage:bool - if true then get the entire content of each mail
            nextPageToken:str - used recursively by function to Loop through next page

        RETURNS:
            :list - a list of emails queried by google
        '''
        service = self.callApi(userId)
        mailList = []
        if service != None:
            results = service.users().messages().list(userId=userId,q=query,pageToken=next_page_token,maxResults=500).execute()
            messages = results.get("messages", [])
            next_page_token = results.get('nextPageToken',None)
            if next_page_token is not None:
                # Recursively check for next page
                mailList += self.getMails(userId,query,getFullMessage,next_page_token)
            if getFullMessage:
                for msg in messages:
                    result = service.users().messages().get(userId=userId, id=msg.get('id')).execute()
                    if result is not None:
                        mailList.append(result)
            else:
                mailList += messages
                
        return mailList
    def batchDelete(self, userId:str, messages:list):
        r'''
        Delete a batch of emails.
        
        PARAMETERS:
            userId:str - mail of affected user.
            messageId:list - Id of messages to send to delete.
        '''
        service = self.callApi(userId)
        if service != None:
            for i in range(0,len(messages),1000):
                body = {"ids":messages[i:(i+1000)]}
                results = service.users().messages().batchDelete(userId=userId,body=body).execute()

    def moveMailToTrash(self, userId:str, messageId:str):
        r'''
        Move one e-mail to trash.
        
        PARAMETERS:
            userId:str - mail of affected user.
            messageId:str - Id of message to send to trash.
        '''
        service = self.callApi(userId)
        if service != None:
            results = service.users().messages().trash(userId=userId,id=messageId).execute()
            msg = messageId + " sent to trash"
            print(msg)