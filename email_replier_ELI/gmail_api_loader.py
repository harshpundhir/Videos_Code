import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pprint import pprint   
import base64
import email
from email.header import decode_header
from datetime import datetime
import re
from email.utils import parseaddr
import json



SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
os.chdir(os.path.dirname(os.path.abspath(__file__)))

creds = None
if os.path.exists("email_token.json"):
    creds = Credentials.from_authorized_user_file("email_token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "creds.json",
            SCOPES,
        )
        creds = flow.run_local_server(port=52873)
    with open("email_token.json", "w") as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

# Fetch messages in inbox
results = service.users().messages().list(
    userId='me',
    labelIds=['INBOX'],
    maxResults=100,
    q='newer_than:100d'  # query to get emails newer than 100 days
).execute()
messages = results.get('messages', [])

email_details = []

for message in messages:
    msg = service.users().messages().get(
        userId='me',
        id=message['id'],
        format='raw'  # Use 'raw' format to get the full email data
    ).execute()
    
    # Decode the email
    msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mime_msg = email.message_from_bytes(msg_str)
    
    # Extract email details
    sender = mime_msg['From']
    name, email_address = parseaddr(sender)
    email_address = email_address.lower()
    subject = mime_msg['Subject']
    date = mime_msg['Date']
    
    # Decode subject if necessary
    decoded_subject = decode_header(subject)[0]
    if isinstance(decoded_subject[0], bytes):
        subject = decoded_subject[0].decode(decoded_subject[1] or 'utf-8')
    else:
        subject = decoded_subject[0]
    
    # Convert date to datetime object
    email_date = email.utils.parsedate_to_datetime(date)
    
    # Extract email body
    body = ""
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            # Skip attachments
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                part_payload = part.get_payload(decode=True)
                if part_payload:
                    body += part_payload.decode(part.get_content_charset() or 'utf-8', errors='ignore')
    else:
        body = mime_msg.get_payload(decode=True).decode(mime_msg.get_content_charset() or 'utf-8', errors='ignore')
    
    url_pattern = r'(https?://\S+|www\.\S+)'  # Pattern to match URLs
    body = re.sub(url_pattern, '', body)
    
    # Optionally, remove any extra whitespace left after URL removal
    body = re.sub(r'\s+', ' ', body).strip()
    email_details.append({ "From": name, "Email": email_address, "Subject": subject,
                            "Date": email_date.strftime('%Y-%m-%d %H:%M:%S'), "Body": body })
    
# save email details to a file
with open('emails_100.json', 'w') as f:
    json.dump(email_details, f, indent=4)
    
