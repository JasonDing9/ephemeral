from datetime import datetime
import json
import os
from agents.mailing import draft_email
from agents.scheduling import create_event
from agents.clarify import search_google
from dotenv import load_dotenv
import subprocess
from speak import speak

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

    elif json_response['action'] == 'link':
        if json_response['link'] != "":
            send_notification(f"Does this link help: {json_response['link']}", json_response["description"])
        
    elif json_response['action'] == 'schedule':
        link = create_event(json_response['attendeeEmails'], json_response['startTime'], json_response['summary'], json_response["description"])
        start_time = datetime.strptime(json_response["startTime"], "%Y-%m-%dT%H:%M:%S")
        start_time = start_time.strftime("%b %d at %I:%M%p")
        send_notification(f"{json_response['summary']} + scheduled at {start_time}. {link}", "Event Scheduled")

    elif json_response['action'] == 'clarify':
        if json_response['result'] != "NONE":
            send_notification(json_response['result'], "Quick Insight")
        else:
            send_notification(search_google(json_response['search_query']), "More Info")

    elif json_response['action'] == 'assistant':
        speak(json_response['answer'])
            
    elif json_response['action'] == 'suggestion':
        if json_response['suggestion'] != []:
            send_notification("\n\n".join(json_response['suggestion']), "Suggestions")