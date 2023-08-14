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
    
def read_yaml(parameter, var):
    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        return(cfg[parameter][var])

def key_listener(stop_event):
    while True:
        if input() == 'q':
            print("Ending Stream")
            stop_event.set()  # Signal the loop to stop
            break

def read_data():
    with open("shared.txt", "r") as file:
        data = file.read()
        return data
    
def get_current_action():
    with open("currentAction.txt", "r") as file:
        data = file.read()
        return data
    
#Save this for memory stuff later
# def respondToChat():

#     keynotes = read_file("keynotes.txt")
#     functions = read_file("functions.txt")
#     load_dotenv()

#     openai.api_key = os.getenv('OPENAI_API_KEY')

#     curr = 0
#     prevs = []

#     question = "who are you?"
#     query = full_query("kianix", [question], 1)
#     memory = query[0]
#     score = query[1]
#     max = random.randint(11, 100)
#     min = random.randint(0, 10)
    
#     #TO DO add a check if memory query value threshold is high, otherwise perhaps dont use the memory as it's not relevant and just make something up
#     if score > .75:
#         if len(prevs) == 0:
#             prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just said this: " + question + ". You have this memory that helps to answer: " + ' '.join(memory) + ". Give a short response. If the memory doesn't help, ignore it. Involve their statement in your response. No emojis. Only ASCII characters. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation. "
#         else:
#             prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just said this: " + question + ". You have this memory that helps to answer: " + ' '.join(memory) + ". Give a short response. If the memory doesn't help, ignore it. Involve their statement in your response. These are your previous statements: " + ' '.join(prevs) + ". Make sure your answer is different and not repetitive from your last statements. No emojis. Only ASCII characters. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation. "
#     else:
#         if len(prevs) == 0:
#             prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just said this: " + question + "Give a short response. Involve their statement in your response. No emojis. Only ASCII characters. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
#         else:
#             prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just said this: " + question + " Give a short response. Involve their statement in your response. If the memory doesn't help, ignore it. These are your previous statements: " + ' '.join(prevs) + ". Make sure your answer is different and not repetitive from your last statements. No emojis. Only ASCII characters. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
    

#     response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages= [{"role": "user", "content": prompt}]
#     )



#     total = response['choices'][0]['message']['content']
#     response_text = total.split("\n")[0]
#     emotion = total.split("\n")[-3].strip().lower()
#     function = total.split("\n")[-1].strip().lower()
#     ans = response_text
#     print(ans)
#     if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
#         send_animation_trigger(emotion)
#     if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
#         send_expression(function)
#     rate = 125 + int(len(ans) * .01)
#     playTTS(ans, rate)
#     save = "Question: " + question + " Response: " + ans
#     if len(save) < 450:
#         insert_memory("kianix", [save])

    


def questionChat(questions):
    #Maybe also add types of questions like, questions about self, questions about chat, questions about streamers, questions about news
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". You've already asked these questions: " + '?'.join(questions) + "Write an interesting question you have not asked yet to your chat. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)


def questionFromChat(text):
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". Someone wrote this in chat. It may contain Twitch emotes: " + text + "Write up a response, comment, question, or sarcastic quip about it. No emojis. ASCII characters only. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)


def generateConversation():
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "Muse to yourself under 50 words. No swearing or controversy. It can be random. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}]
    )

    #Probably need to save the questions

    total = response['choices'][0]['message']['content']
    response_text = total.split("\n")[0]
    emotion = total.split("\n")[-1].strip().lower()
    ans = response_text

    total = response['choices'][0]['message']['content']
    response_text = total.split("\n")[0]
    emotion = total.split("\n")[-3].strip().lower()
    function = total.split("\n")[-1].strip().lower()
    ans = response_text
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)

def generateJoke():
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "Generate a random joke based on a random topic. Do not ask: Why don't scientists trust atoms?. Add the punchline after you say the joke. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation. "
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)

def generateSelfTalk():
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    backstory = read_file("backstory.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics: " + ' '.join(keynotes) + "This is your backstory: " + ' '.join(backstory) + ". Reminisce on a made-up story from the past under 60 words. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)

def emote():
    send_expression("turnoffsigil()")

def sayGoodbye():
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". Tell your stream you have to go and thank them for watching the stream. No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)


def startStream(plans):
    keynotes = read_file("keynotes.txt")
    functions = read_file("functions.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". You are starting your stream. Welcome chatters to your stream. Talk about your plans for the day and the future: " + plans + " No swearing or controversy. After your response, categorize yourself as either curious, thinking, uneasy, shocked, pleased, surprised, happy, amazed, or sorrow and write it as only one of those words after a new line no punctuation. You have this set of abilities that are encoded as parameters: " + ' '.join(functions) + ". If you call a function, you will perform the action that it describes. Each function is separated from its description by a ':' and separated from other functions by a ';' After categorizing your response, simply call one function using its name and '()' and write it after a new line no punctuation."
        

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
    print(ans)
    if emotion in ["curious", "thinking", "uneasy", "shocked", "pleased", "surprised", "happy", "amazed", "sorrow"]:
        send_animation_trigger(emotion)
    if function in ["stars()","hearts()", "cry()", "turnoffsigil()", "default()", "blureyes()", "powerstate()", "noflowers()"]:
        send_expression(function)
    rate = 125 + int(len(ans) * .01)
    playTTS(ans, rate)

