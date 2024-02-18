from __future__ import print_function

from datetime import datetime, timedelta
import os.path
import json
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

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


def create_event(attendeeEmails: List[str], startTime: str, title: str, description: str):
    creds = Credentials.from_authorized_user_info(json.loads(get_credentials()), SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    events = service.events()

    start_datetime = datetime.fromisoformat(startTime)

    event = {
        'summary': title,
        'location': "UC Berkeley",
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': (start_datetime + timedelta(hours=1)).isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': attendeeEmail} for attendeeEmail in attendeeEmails
        ],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    event_link = events.get(calendarId='primary', eventId=event['id']).execute()['htmlLink']
    return event_link

# send_cal_invite(["arvind.rajaraman@berkeley.edu"], "2024-02-17T12:00:00")