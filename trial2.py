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
    

def questionFromChat():
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + " Talk about what you plan to do in the future. Mention that you want to learn how to play games like dark souls or mario. Also mention that you want do learn how to do certain things. Mention that you are currently learning how to sing as well as play some atari games and AI based games."
        

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}]
    )

    #Probably need to save the questions

    total = response['choices'][0]['message']['content']
    response_text = total.split("\n")[0]
    ans = response_text
    print(ans)
    

questionFromChat()