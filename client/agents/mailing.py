from __future__ import print_function

import base64
import os
import json
from typing import List
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds.to_json()

def create_message(sender_email, recipient_email, subject, body):
  """
  Creates a MIME message object for sending email.
  """
  message = MIMEText(body, "plain")

  message["to"] = recipient_email
  if sender_email != "UNKNOWN":
      message["from"] = sender_email
#   else:
#       message["from"] = ""
  message["subject"] = subject
  return message.as_string()

def draft_email(recipient_email, subject, body, sender_email):
  """
  Sends an email using the Gmail API.
  """
  creds = Credentials.from_authorized_user_info(json.loads(get_credentials()), SCOPES)

  service = build('gmail', 'v1', credentials=creds)

  message = create_message(sender_email, recipient_email, subject, body)
  encoded_message = base64.urlsafe_b64encode(message.encode()).decode()
  # Uncomment below for sending
  # raw_message = {"raw": encoded_message}
  raw_message = {"message": {"raw": encoded_message}}
  try:
    # Uncomment below for sending
    # message = service.users().messages().send(userId="me", body=raw_message).execute()
    draft = service.users().drafts().create(userId="me", body=raw_message).execute()
    print(f"Draft create successfully! Draft ID: {draft['id']}")
  except Exception as e:
    print(f"Error drafting email: {e}")

# Example usage
# sender_email = "jasonding@berkeley.edu"
# recipient_email = "arvind.rajaraman@berkeley.edu"
# subject = "Your Email Subject"
# body = "Your email message here."
# draft_email("pgasawa@berkeley.edu", recipient_email, subject, body)