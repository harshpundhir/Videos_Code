import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from langchain_google_community import GMailLoader
from langchain_community.chat_loaders.utils import (
    map_ai_messages,
)
from pprint import pprint
import json
from langchain_core.messages.base import message_to_dict

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# code to cd to email_replier_ELI directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("email_token.json"):
    creds = Credentials.from_authorized_user_file("email_token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            # your creds file here. Please create json file as here https://cloud.google.com/docs/authentication/getting-started
            "creds.json",
            SCOPES,
        )
        creds = flow.run_local_server(port=52873)
    # Save the credentials for the next run
    with open("email_token.json", "w") as token:
        token.write(creds.to_json())

loader = GMailLoader(creds=creds, n=20)
emails = loader.load()

for email in emails:
    # print(email["functions"])
    pprint(email["messages"])