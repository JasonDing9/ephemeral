import together
import os
from rag import query
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

def send_email(context):
    rag_context = query(context, "context-vectorstore.pkl")
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")
    prompt = f"""
You are an AI assistant for helping to write emails. Given the following meeting conversation, please write a one or two sentence email given the following conversation. Please just return a JSON response. If you do not know the reciepient's email address, put UNKNOWN in the recipient field. 
    
Example email #1:
Conversation: Ayushi said: Yeah, I'll send an email to Parth for a one-on-one call.
JSON Response:
{{
    'recipient': 'pgasawa@berkeley.edu',
    'subject': 'One-on-One Chat',
    'body': 'Hi Parth, \nDo you have time for a one-on-one chat tomorrow?\n Best,\n Ayushi',
}}
    
Example email #2:
Conversation: Jason said: I'll send an email to ask Arvind if the classification model has finished trainining.
JSON Response:
{{
    'recipient': 'arvind.rajaraman@berkeley.edu',
    'subject': 'Classification Model Inquiry',
    'body': 'Hi Arvind, \nIs the classification model finished training?\n Best,\n Jason',
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
    return json_result


send_email("Arvind said: I will send an email to Jason to remind him to finish the project by this Friday.")