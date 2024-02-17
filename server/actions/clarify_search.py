import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def clarify_search(context):
    rag_context = query(context, "context-vectorstore.pkl")
    rag_contacts_context = query(context, "contacts-vectorstore.pkl")
    prompt = f"""
    You are an AI assistant who will help answer a question. 
    The following conversation will contain a question within it. 
    Your job is to answer the question using the context that will be provided to you below.   
    Please just return a JSON response.
    If you are unable to answer the question based on the context provided, please just return NONE for result and a corresponding Google search query for the answer.
    
    Example question #1:
    Conversation: Ayushi said: When is the project due?
    JSON Response:
    {{
    "result": "It is due on December 18, 2024.",
    "search_query": "NONE"
    }}

    Example question #1:
    Conversation: Jason said: What do you mean by multithreading?
    JSON Response:
    {{
    "result": "NONE",
    "search_query": "multithreading definition"
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

    json_result['action'] = 'clarify'

    return json.dumps(json_result)
