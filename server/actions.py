import together
import os
from rag import query
from dotenv import load_dotenv
from agents.mailing import draft_email
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def create_email(context):
    rag_context = query(context, "context-vectorstore.pkl")
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")
    prompt = f"""
You are an AI assistant for helping to write emails. Given the following meeting conversation, please write a one or two sentence email given the following conversation. Please just return a JSON response. If you do not know the reciepient's email address, put UNKNOWN in the recipient field. 
    
Example email #1:
Conversation: Ayushi said: Yeah, I'll send an email to Parth for a one-on-one call.
JSON Response:
{{
    "recipient": "pgasawa@berkeley.edu",
    "subject": "One-on-One Chat",
    "body": "Hi Parth,\\n\\nDo you have time for a one-on-one chat tomorrow?\\n\\nBest,\\nAyushi"
}}
    
Example email #2:
Conversation: Jason said: I'll send an email to ask Arvind if the classification model has finished trainining.
JSON Response:
{{
    "recipient": "arvind.rajaraman@berkeley.edu",
    "subject": "Classification Model Inquiry",
    "body": "Hi Arvind,\\n\\nIs the classification model finished training?\\n\\nBest,\\nJason"
}}
    
========
{rag_context}
{rag_contacts_context}
========
    
Conversation: {context}
    """
    
    print(prompt)
    print("===============")
    
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
    if not response.find("{") or not response.find("}"):
        return -1
    json_result = response[response.find("{"):response.find("}")+1]
    print(json_result)
    
    json_result = json.loads(json_result)
    draft_email(json_result["recipient"], json_result["subject"], json_result["body"], USER_EMAIL)
    return json_result


create_email("Jason said: I will send an email to Arvind to remind him to finish the project by this Friday.")