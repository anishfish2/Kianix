from full_query import full_query
from insert_memory import insert_memory
import openai
from dotenv import load_dotenv
import os
import yaml
import random
import time
from kianix_functions import respondToChat, questionChat, questionFromChat, generateConversation, generateJoke, generateSelfTalk, emote


def main():
    askedQuestions = []
    textFromChat = "Can you soap my mouth Flushed"
    while True:
        decision = random.randint(0, 6)
        if decision == 0:
            print("Chat question:")
            respondToChat(1)
        elif decision == 1:
            questionChat(askedQuestions)
            time.sleep(3)
        elif decision == 2:
            print("User said this: " +  textFromChat)
            questionFromChat(textFromChat)
        elif decision == 3:
            generateConversation()
        elif decision == 4:
            generateJoke()
        elif decision == 5:
            generateSelfTalk()
        elif decision == 6:
            emote()



if __name__ == '__main__':
    main()