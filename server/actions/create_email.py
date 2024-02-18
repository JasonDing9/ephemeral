import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def create_email(context):
    rag_context = query(context, "context-vectorstore.pkl")
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")
    prompt = f"""
You are an AI assistant for helping to write emails. Given the following meeting conversation, please write a one or two sentence email given the following conversation. Please just return a JSON response. If you do not know the reciepient's email address, put "UNKNOWN" in with quotes the recipient field. For the body, please use \\n characters and not a new line.
    
Example email #1:
Conversation: Ayushi said: Yeah, I'll send an email to Parth for a one-on-one call.
JSON Response:
{{
    "recipient": "pgasawa@berkeley.edu",
    "subject": "One-on-One Chat",
    "body": "Hi Parth,\\n\\nDo you have time for a one-on-one chat tomorrow?\\n\\nBest,\\nAyushi"
}}
    
Example email #2:
Conversation: Jason said: I'll send an email to ask Arvind if the classification model has finished training.
JSON Response:
{{
    "recipient": "arvind.rajaraman@berkeley.edu",
    "subject": "Classification Model Inquiry",
    "body": "Hi Arvind,\\n\\nIs the classification model finished training?\\n\\nBest,\\nJason"
}}

Example email #3:
Conversation: Can everyone open the Tree Hacks slack?
JSON Response:
{{
    "recipient": "UNKNOWN",
    "subject": "Tree Hacks Slack",
    "body": "Hi everyone,\n\nCan you open the Tree Hacks slack?\n\nBest"
}}
    
========
{rag_context}
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
                max_tokens = 512,
                temperature = 0.7,
                top_k = 50,
                top_p = 0.7,
                repetition_penalty = 1,
                stop = ["[INST]"],
                safety_model = "",
            )

            # print generated text
            response = output['output']['choices'][0]['text']
            if response.find("{") == -1 or response.find("}") == -1:
                raise Exception("Sorry, no JSON object to be found")
            json_result = response[response.find("{"):response.find("}")+1]
            print(json_result)
            
            json_result = json.loads(json_result)
            json_result["action"] = "email"
            success = True
        except:
            print("An error occured. Retrying...")
            pass
        
        if success:
            break

    return json.dumps(json_result)

# create_email("Parth said: I will send an email to Arvind to remind him to finish the project by this Friday.")