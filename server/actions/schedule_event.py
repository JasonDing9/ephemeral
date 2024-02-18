from datetime import datetime, timedelta
import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def create_event(context):
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")

    current_day = datetime.now().strftime("%A, %B %d, %Y")
    tomorrow_2pm = (datetime.now() + timedelta(days=1)).replace(hour=14, minute=0, second=0, microsecond=0).isoformat()
    tomorrow_3pm = (datetime.now() + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0).isoformat()
    prompt = f"""
You are an AI assistant for helping to schedule a calendar event if needed, by listening to meeting conversations. Given the following meeting conversation, please write a JSON object with details about the calendar event. Please just return a JSON response. Note that today is {current_day} If you cannot determine a summary or description for the event, then just write Meeting. If information about date is not given, then assume it is tomorrow. If information about time is not given, then assume it is 2 PM. If information about the length of the meeting is not given, then assume it is 1 hour long. Regarding attendees, try to figure out who is relevant to the meeting from context (through words like "one-on-one", "all", "just us three", etc.). If not enough information is given about this, then invite everyone.
    
Example calendar event #1:
Conversation: Ayushi said: Let's all meet tomorrow 2 PM to discuss sprint planning for this project.
JSON Response:
{{
    "summary": "Team Sprint Planning ✏️",
    "description": "Team sprint planning",
    "startTime": "{tomorrow_2pm}",
    "duration": "60 min",
    "attendeeEmails": ["arvind.rajaraman@berkeley.edu", "pgasawa@berkeley.edu", "ayushi.batwara@berkeley.edu", "jasonding@berkeley.edu"]
}}
    
Example calendar event #2:
Conversation: Arvind said: I will meet one-on-one with you Ayushi tomorrow 2 PM to debug the code, so that we can have it ready in time for the production release.
JSON Response:
{{
    "summary": "Jason / Arvind Debugging Session 🐛",
    "description": "Team sprint planning",
    "startTime": "{tomorrow_2pm}",
    duration": "60 min",
    "attendeeEmails": ["arvind.rajaraman@berkeley.edu", "ayushi.batwara@berkeley.edu"]
}}
    
========
Here is everyone's contact information:
{rag_contacts_context}
========
    
Conversation: {context}
    """
    success = False
    json_result = None
    for i in range(3):
        try:
            output = together.Complete.create(
                prompt = f"[INST] {prompt} [/INST]",
                model = "meta-llama/Llama-2-70b-chat-hf", 
                max_tokens = 2048,
                temperature = 0.7,
                top_k = 50,
                top_p = 0.7,
                repetition_penalty = 1,
                stop = ["[INST]"],
                safety_model = "",
            )

            # print generated text
            response = output['output']['choices'][0]['text']
            if not response.find("{") or not response.find("}"):
                raise Exception("Sorry, no JSON object to be found")
            json_result = response[response.find("{"):response.find("}")+1]
            print(json_result)
            
            json_result = json.loads(json_result)
            json_result["action"] = "schedule"
            success = True
        except:
            print("An error occured. Retrying...")
            pass 
        
        if success:
            break

    return json.dumps(json_result)