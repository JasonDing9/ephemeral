import together
import os
from actions.rag import query
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def get_suggestions():
    log = open("actions/central-log.txt", "r")
    recent_central_log = "".join(log.readlines()[-5:])
    
    rag_context = query(recent_central_log, "context-vectorstore.pkl")
    prompt = f"""
You are an AI assistant who helps creates suggestions for topics, additional discussion questions, and answers for the current conversation. Begin your suggestions with "AI assisstant said: ". Given the following meeting conversation, please give suggestions for how to continue or answer the conversation. Please just return a JSON response. Put each possible suggestion in an array, and make sure all arguments in the JSON response is in quotations. If you do not thing you have any solid suggestions, put an empty list in the JSON's suggestion field.
    
Example #1:
Conversation:
Ayushi said: Do you know how multithreading works?
Jason said: Yeah, multi threading is the processor can switch between different threads and execute several threads at the same time.
Ayushi said: Is multi threading always better than single threading?
Jason said: I think multi threading is typically better in the right cases, but not always. What do you think, AI assisstant?
JSON Response:
{{
    "suggestion": ["AI Assisstant said: What Jason is true. To go more into depth, multi threading is typically better when tasks can be executed concurrently and not need to wait for each other. If tasks cannot be executed concurrently, then the additional overhead from multi threading may make it slower than single threading.", "AI Assisstant said: In what cases do you think multi threading would be slower than single threading? Think about concepts such as critical sections and synchronization."]
}}
    
Example #2:
Conversation: 
Parth said: What project related to AI agents do you think we could work on for our Tree Hack's project?
Jason said: What about a project that can help city governments connect with other cities that have faced similar governence problems?
Parth said: Hmm, I think that might work, but I'm not sure if I would be that interested in the project and I'm not sure if that project would be very impressive.
Jason said: I suppose that's true. Have any ideas?
Parth said: I'm don't know.
JSON Response:
{{
    "suggestion": ["AI Assisstant said: What about a project for meetings that will listen to the audio use an ML agent to automatically do common tasks such as sending emails or scheduling meetings for higher productivity.", "AI Assisstant said: One idea could be to create an agent that can automatically carry operations on your OS such as opening files or controlling your music."]
}}

Example #3:
Conversation:
{{
    "suggestion": ["AI Assisstant said: Hello, how is everyone doing today?"]
}}
    
========
{rag_context}
========
    
Conversation: {recent_central_log}
    """
    success = False
    for i in range(3):
        output = together.Complete.create(
            prompt = f"[INST] {prompt} [/INST]",
            model = "meta-llama/Llama-2-70b-chat-hf", 
            max_tokens = 1024,
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
        
        try:
            json_result = json.loads(json_result)
            json_result["action"] = "suggestion"
            success = True
        except:
            pass
        
        if success:
            break

    return json.dumps(json_result)