
import openai
from dotenv import load_dotenv
import os




print("got here")

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

prompt = "Say hello to me"
    
print("got here 2")
response = openai.ChatCompletion.create(
model="gpt-4",
messages= [{"role": "user", "content": prompt}]
).choices[0].message.content
print(response)
print("got here 3")