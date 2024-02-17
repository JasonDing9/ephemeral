import json
import os
from agents.mailing import draft_email
from dotenv import load_dotenv
import subprocess

load_dotenv()

USER_EMAIL = os.environ["USER_EMAIL"]

def send_notification(message, title="Notification Title"):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def handle_response(response: str):
    json_response = json.loads(response)
    if json_response['action'] == 'email':
        draft_email(json_response['recipient'], json_response['subject'], json_response['body'], USER_EMAIL)
        send_notification("Email drafted to " + json_response['recipient'] + " regarding " + json_response["subject"], "Email Drafted")