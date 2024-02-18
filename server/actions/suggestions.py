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
    
    prompt = f"""
You are an AI assistant who helps creates suggestions for topics, additional discussion questions, coaching tips, and answers for the current conversation. Begin your suggestions with "AI assisstant said: ". Given the following meeting conversation, please give two to three suggestions for how to continue or answer the conversation. Please just return a JSON response. Put each possible suggestion in an array, and make sure all arguments in the JSON response is in quotations. If you do not think you have any solid suggestions, put an empty list in the JSON's suggestion field. In the case that the conversation seems to be ending soon, make sure to suggest to setup a follow-up meeting or action items to do.
    
Example #1:
Conversation:
Ayushi said: Do you know how multithreading works?
Jason said: Yeah, multi threading is the processor can switch between different threads and execute several threads at the same time.
Ayushi said: Is multi threading always better than single threading?
Jason said: I think multi threading is typically better in the right cases, but not always.
JSON Response:
{{
    "suggestion": ["AI Assisstant said: What Jason said is true. To go more into depth, multi threading is typically better when tasks can be executed concurrently and not need to wait for each other. If tasks cannot be executed concurrently, then the additional overhead from multi threading may make it slower than single threading.", "AI Assisstant said: In what cases do you think multi threading would be slower than single threading? Think about concepts such as critical sections and synchronization."]
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
    "suggestion": ["AI Assisstant said: What about a project for meetings that will listen to the audio use an ML agent to automatically do common tasks such as sending emails or scheduling meetings for higher productivity.", "AI Assisstant said: One idea could be to create an agent that can automatically carry operations on your OS such as opening files or controlling your music.", "AI Assisstant said: What if you all thought about a specific category such as education, health, or gaming and went from there? Is there any specific topics that everyone is interest in?"]
}}

Example #3:
Conversation:
{{
    "suggestion": ["AI Assisstant said: How is everyone doing today?", "AI Assistant said: To break the ice, share one thing you are looking forward to this week."]
}}

Example #4:
Ayushi: Would you be able to send me the link to the project later?
Parth: Yeah, sure! Before we wrap up, do you have any additional questions?
Ayushi: No, I think I'm good.
Parth: Ok, sounds good! It was nice talking with you.
Conversation:
{{
    "suggestion": ["AI Assisstant said: Schedule a follow up meeting to talk more about the project, "AI Assistant said: Reiterate your action items before the next meeting, such as sending the project link to Ayushi."]
}}
    
========
    
Conversation: {recent_central_log}
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
            if response.find("{") == -1 or response.find("}") == -1:
                raise Exception("Sorry, no JSON object to be found")
            json_result = response[response.find("{"):response.find("}")+1]
            print(json_result)
            
            json_result = json.loads(json_result)
            json_result["action"] = "suggestion"
            success = True
        except:
            print("An error occured. Retrying...")
            pass
        
        if success:
            break

    return json.dumps(json_result)