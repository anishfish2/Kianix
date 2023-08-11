import openai
from dotenv import load_dotenv
import os
import threading
from texttospeech import *
from live2D import *
import sys
def process_chunk(content):
    if content is not None:
        print(content, end=';')
        # Open a new thread and call the playTTS function
        thread = threading.Thread(target=playTTS, args=(content,125))
        thread.start()

#To do add a current action thing so that in the future u can add a comment on action function
def read_file(path_to_file):
    with open(path_to_file) as f:
        contents = ' '.join(f.readlines())
        return contents
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
keynotes = read_file("keynotes.txt")
functions = read_file("functions.txt")
prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". Generate a random joke. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation. "
chunks = ""
for chunk in openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}],
    stream=True,
):
    content = chunk["choices"][0].get("delta", {}).get("content") + ' '.join(chunks)
    if content is not None:
        print(content)
        #sys.stdout.write(content)
        process_chunk(content)
    else :
        chunks += content
    
