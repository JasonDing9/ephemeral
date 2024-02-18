import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def get_link(context):
    rag_context = query(context, "context-vectorstore.pkl")
    rag_links_context = query(context, "links-vectorstore.pkl")
    prompt = f"""
You are an AI assistant to help retrieve relevent link. Given the following meeting conversation, please determine if there is a corresponding link related to it. Please just return a JSON response and make sure there are quotes around the link. If there is no closely related link to the conversation, make sure to not falsely return a link. Instead, please return an empty string for the link. 
    
Example #1:
Conversation: Arvind said: Can everyone open up our Tree Hack's project ideation doc?
JSON Response:
{{
    "description": "Tree Hacks Project Ideation Doc",
    "link": "https://docs.google.com/document/d/1eXAcPF0r35dyT_zn38gOPHIMLsN2G1MxM8f-rjSWodY/edit"
}}
    
Example #2:
Conversation: Jason said: If you look in our Tree Hack's project GitHub repo, you can find the file.
JSON Response:
{{
    "description": "Tree Hacks Project GitHub Rego",
    "link": "https://github.com/pgasawa/treehacks24-dev"
}}

Example #3:
Conversation: Parth said: The Wikipedia page on cattle says that they are usually raised for meat, dairy products, and leather.
JSON Response:
{{
    "description": "",
    "link": ""
}}
    
========
{rag_context}

Potential Relevent Links:
{rag_links_context}
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
            if not response.find("{") or not response.find("}"):
                raise Exception("Sorry, no JSON object to be found")
            json_result = response[response.find("{"):response.find("}")+1]
            print(json_result)
            
            json_result = json.loads(json_result)
            json_result["action"] = "link"
            success = True
        except:
            print("An error occured. Retrying...")
            pass 
        
        if success:
            break

    return json.dumps(json_result)