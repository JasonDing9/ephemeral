import together
import os
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

def send_email():
    prompt = """
    Given the following meeting conversation, please write a one or two sentence email given the following context. Please just return a JSON response, for example:
    \{
        "recipient": "pgasawa@berkeley.edu",
        "subject": "One-on-One Chat",
        "body": "Hi Parth, \nI hope you are doing well! Do you have time for a one-on-one chat tomorrow?\n Best,\n Ayushi",
    \}
    If you do not know the reciepient's email address, put UNKNOWN in the recipient field.
    """
    context = "I will send an email to Jason to remind him to finish the project by this Friday."
    
    output = together.Complete.create(
        prompt = f"[INST] {prompt}{context} [/INST]",
        model = "meta-llama/Llama-2-13b-chat-hf", 
        max_tokens = 512,
        temperature = 0.7,
        top_k = 50,
        top_p = 0.7,
        repetition_penalty = 1,
        stop = ["[INST]"],
        safety_model = "",
    )

    # print generated text
    print(output['output']['choices'][0]['text'])

send_email()