import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def clarify_search(context):
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")
    prompt = f"""
    You are an AI assistant who will help answer a question. 
    The following conversation will contain a question within it. 
    Your job is to answer the question using the context that will be provided to you below.   
    Please just return a JSON response.
    If you are unable to answer the question based on the context provided, please just return NONE for result and a corresponding Google search query for the answer.
    
    Example question #1:
    Conversation: Ayushi said: I'm not familiar with cyber attacks - can you explain it more?
    JSON Response:
    {{
    "result": "A cyber attack is a malicious and intentional attempt by an individual, group, or organization to exploit vulnerabilities in computer systems, networks, or digital infrastructure to compromise data, disrupt operations, or gain unauthorized access. Cyber attacks encompass a wide range of techniques, including malware deployment, phishing, denial-of-service attacks, and other methods aimed at compromising the confidentiality, integrity, or availability of digital assets.",
    "search_query": "NONE"
    }}

    Example question #2:
    Conversation: Jason said: What is the current stock price of Apple?
    JSON Response:
    {{
    "result": "NONE",
    "search_query": "Apple stock price"
    }}

    Example question #3:
    Conversation: Parth said: What is the capital of Missouri?
    JSON Response:
    {{
    "result": "The capital of Missouri is Jefferson City.",
    "search_query": "NONE"
    }}

    ========
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
            json_result['action'] = 'clarify'
            success = True
        except:
            print("An error occured. Retrying...")
            pass 
        
        if success:
            break

    return json.dumps(json_result)
