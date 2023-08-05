from full_query import full_query
from insert_memory import insert_memory
import openai
from dotenv import load_dotenv
import os
import yaml
import random
import time


def read_file(path_to_file):
    with open(path_to_file) as f:
        contents = ' '.join(f.readlines())
        return contents
    
def read_yaml(parameter, var):
    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        return(cfg[parameter][var])
    
def respondToChat(numResponses):

    keynotes = read_file("keynotes.txt")

    load_dotenv()

    openai.api_key = os.getenv('OPENAI_API_KEY')

    curr = 0
    prevs = []
    while curr != numResponses:
        question = input()

        query = full_query("kianix", [question], 1)
        memory = query[0]
        score = query[1]
        max = random.randint(11, 100)
        min = random.randint(0, 10)
        #TO DO add a check if memory query value threshold is high, otherwise perhaps dont use the memory as it's not relevant and just make something up
        if score > .75:
            if len(prevs) == 0:
                prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just asked you this question: " + question + ". You have this memory that helps to answer the question: " + ' '.join(memory) + ". Give a short response to the question. If the memory doesn't help, ignore it. Involve the question in your response. No emojis. Only ASCII characters."
            else:
                prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just asked you this question: " + question + ". You have this memory that helps to answer the question: " + ' '.join(memory) + ". Give a short response to the question. If the memory doesn't help, ignore it. Involve the question in your response. These are your previous statements: " + ' '.join(prevs) + ". Make sure your answer is different and not repetitive from your last statements. No emojis. Only ASCII characters."
        else:
            if len(prevs) == 0:
                prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just asked you this question: " + question + "Give a short response to the question. Involve the question in your response. No emojis. Only ASCII characters."
            else:
                prompt = "Write a " + str(min) + "-" + str(max) + " word response as if you were this person:" + ' '.join(keynotes) + " Your Twitch chat just asked you this question: " + question + " Give a short response to the question. Involve the question in your response. If the memory doesn't help, ignore it. These are your previous statements: " + ' '.join(prevs) + ". Make sure your answer is different and not repetitive from your last statements. No emojis. Only ASCII characters."
        

        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages= [{"role": "user", "content": prompt}]
        )



        ans = response['choices'][0]['message']['content']
        save = "Question: " + question + " Response: " + ans
        
        if len(save) < 450:
            insert_memory("kianix", [save])

        print(ans)
        
        prevs.append(ans)
        curr += 1

def questionChat(questions):
    #Maybe also add types of questions like, questions about self, questions about chat, questions about streamers, questions about news
    keynotes = read_file("keynotes.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". You've already asked these questions: " + '?'.join(questions) + "Write a new unrelated question that is not about gaming you have not asked yet to the chat that you are streaming to."
        

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}]
    )

    #Probably need to save the questions

    ans = response['choices'][0]['message']['content']

    print(ans)
    
def questionFromChat(text):
    keynotes = read_file("keynotes.txt")
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    prompt = "You are a vtuber with these characteristics and backstory: " + ' '.join(keynotes) + ". Someone wrote this in chat. It may contain Twitch emotes: " + text + "Write up a response, comment, question, or sarcastic quip about it. No emojis. ASCII characters only."
        

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages= [{"role": "user", "content": prompt}]
    )

    #Probably need to save the questions

    ans = response['choices'][0]['message']['content']

    print(ans)


def emote():
    print("Smile")


def main():
    askedQuestions = []
    textFromChat = "Can you soap my mouth Flushed"
    while True:
        decision = random.randint(0, 2)
        if decision == 0:
            print("Chat question:")
            respondToChat(1)
        elif decision == 1:
            questionChat(askedQuestions)
            time.sleep(3)
        elif decision == 2:
            print("User said this: " +  textFromChat)
            questionFromChat(textFromChat)


if __name__ == '__main__':
    main()