import together
import os
from dotenv import load_dotenv
import json

load_dotenv()
together.api_key = os.environ['TOGETHER_API']
USER_EMAIL = os.environ['USER_EMAIL']

def assistant(question: str):
    log = open("actions/central-log.txt", "r")
    recent_central_log = "".join(log.readlines()[-4:])
    
    prompt = f"""
You are an AI assistant who helps answers questions that arise in a conversation when asked. Please give an answer to the question as a JSON response. Make sure all arguments in the JSON response are in quotations. If you do not think you have an answer, please say you're not sure in the answer field.
    
Example #1:
Prior Conversation:
Ayushi said: Do you know how multithreading works?
Jason said: Yeah, multi threading is the processor can switch between different threads and execute several threads at the same time.
Ayushi said: Is multi threading always better than single threading?
Question: Jason said: I think multi threading is typically better in the right cases, but not always. What do you think, AI assisstant?
JSON Response:
{{
    "answer": "What Jason said is true. To go more into depth, multi threading is typically better when tasks can be executed concurrently and not need to wait for each other. If tasks cannot be executed concurrently, then the additional overhead from multi threading may make it slower than single threading."
}}
    
Example #2:
Prior Conversation: 
Parth said: What project related to AI agents do you think we could work on for our Tree Hack's project?
Jason said: What about a project that can help city governments connect with other cities that have faced similar governence problems?
Parth said: Hmm, I think that might work, but I'm not sure if I would be that interested in the project.
Jason said: That's fair. Have any ideas?
Question: Parth said: I'm don't know. Assistant, do you have any ideas?
JSON Response:
{{
    "answer": "What about a project for meetings that will listen to the audio use an ML agent to automatically do common tasks such as sending emails or scheduling meetings for higher productivity."
}}
    
========
    
Prior Conversation: {recent_central_log}
Question: {question}
JSON Response:
    """
    success = False
    json_result = None
    for i in range(3):
        try:
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
                raise Exception("Sorry, no JSON object to be found")
            json_result = response[response.find("{"):response.find("}")+1]
            print(json_result)
            
            json_result = json.loads(json_result)
            json_result["action"] = "assistant"
            success = True
        except:
            print("An error occured. Retrying...")
            pass 
        
        if success:
            break

    return json.dumps(json_result)