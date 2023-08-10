from full_query import full_query
from insert_memory import insert_memory
import openai
from dotenv import load_dotenv
import os
import yaml
from texttospeech import *
from live2D import *
import random
def read_file(path_to_file):
    with open(path_to_file) as f:
        contents = ' '.join(f.readlines())
        return contents
keynotes = read_file("keynotes.txt")
functions = read_file("functions.txt")
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

while True:
    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". Generate a random thought that anyone could have while going about their day. No swearing or controversy. It can be random. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation. "
        

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}]
    )

    #Probably need to save the questions


    total = response['choices'][0]['message']['content']
    response_text = total.split("\n")[0]
    emotion = total.split("\n")[-3].strip().lower()
    function = total.split("\n")[-1].strip().lower()
    ans = response_text
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)