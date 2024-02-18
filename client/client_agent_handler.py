from datetime import datetime
import json
import base64
import os
from agents.mailing import draft_email
from agents.scheduling import create_event
from agents.clarify import search_google
from dotenv import load_dotenv
import subprocess
from speak import speak

load_dotenv()

USER_EMAIL = os.environ["USER_EMAIL"]

def write_to_file(notification):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = "../flask/data/" + timestamp + ".json"
    with open(file_path, "w") as file:
        # Write just the JSON object as is
        file.write(json.dumps(notification))
        file.write("\n")

def send_notification(message, title="Notification Title"):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def handle_response(response: str):
    try:
        json_response = json.loads(response)
    except Exception as e:
        print("JSON failed to load")
        print(e)
        return
    notification = {}
    
    try:
        if json_response['action'] == 'email':
            draft_email(json_response['recipient'], json_response['subject'], json_response['body'], USER_EMAIL)
            json_response['creation_time'] = datetime.now().isoformat()
            write_to_file(json_response)

        elif json_response['action'] == 'link':
            if json_response['link'] != "":
                json_response['creation_time'] = datetime.now().isoformat()
                write_to_file(json_response)
            
        elif json_response['action'] == 'schedule':
            link = create_event(json_response['attendeeEmails'], json_response['startTime'], json_response['summary'], json_response["description"])
            start_time = datetime.strptime(json_response["startTime"], "%Y-%m-%dT%H:%M:%S")
            start_time = start_time.strftime("%b %d at %I:%M%p")
            json_response['start_time'] = start_time
            json_response["link"] = link
            json_response['creation_time'] = datetime.now().isoformat()
            write_to_file(json_response)

        elif json_response['action'] == 'clarify':
            if json_response['result'] != "NONE":
                json_response['creation_time'] = datetime.now().isoformat()
                write_to_file(json_response)

        elif json_response['action'] == 'assistant':
            speak(json_response['answer'])
                
        elif json_response['action'] == 'suggestion':
            if json_response['suggestion'] != []:
                json_response['creation_time'] = datetime.now().isoformat()
                write_to_file(json_response)
                
        elif json_response['action'] == 'end':
            bytes = bytes.fromhex(json_response['bytes'])
            decodeit = open('image.png', 'wb') 
            decodeit.write(base64.b64decode((bytes))) 
            decodeit.close() 
            
            try:
                # Open the image in the default image viewer
                subprocess.run(["open", 'image.png'])
            except FileNotFoundError:
                print("Error: Default image viewer not found.")
            
            
    except Exception as e:
        print("An error has occured in the handler.")
        print(e)
