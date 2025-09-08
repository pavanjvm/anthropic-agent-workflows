from openai import OpenAI
from dotenv import load_dotenv
from system_prompt import prompt_chaining
import json
load_dotenv()
client = OpenAI()

response = client.responses.create(model='gpt-5',input=prompt_chaining)

result = json.loads(response.output_text)

print(result)




