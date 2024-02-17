import together
import os
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.environ['TOGETHER_API']

# see available models
model_list = together.Models.list()

print(f"{len(model_list)} models available")

# print the first 10 models on the menu
model_names = [model_dict['name'] for model_dict in model_list]
print(model_names[:10])

prompt = "I will send an email to Jason."
output = together.Complete.create(
  prompt = f"<human>: {prompt}\n<bot>:", 
  model = "meta-llama/Llama-2-70b-hf", 
  max_tokens = 256,
  temperature = 0.8,
  top_k = 60,
  top_p = 0.6,
  repetition_penalty = 1.1,
  stop = ['<human>', '\n\n']
)

# print generated text
print(output['output']['choices'][0]['text'])