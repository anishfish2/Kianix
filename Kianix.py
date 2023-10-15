from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import random
import redis
    

# def kianix_awake(stop_event):
def kianix_awake():
    askedQuestions = []

    time_awoken = time.time()
    
    redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    plans = read_plans(redis_server)

    startStream(plans)

    try:
        current_time = time.time()
        elapsed_time = current_time - time_awoken

        nothingUrgent = True
        
        if nothingUrgent:
            #If new chat
            currChat = read_chat(redis_server)
            choice = random.randint(0, 10)
            
            if choice <= 9 and currChat != None:
                print("User said: " + currChat)
                questionFromChat(currChat)
            else:
                decision = random.randint(0, 4)
                if decision == 0:
                    print("questioning chat")
                    askedQuestions += questionChat(askedQuestions)
                    
                elif decision == 3:
                    print("making conversation")
                    generateConversation()
                
                elif decision == 4:
                    print("generating joke")
                    generateJoke()

                elif decision == 5:
                    print("talking to myself")
                    generateSelfTalk()

                elif decision == 6:
                    emote()
    except:
        print("Some Error Happened -> Restarting")
        #continue

#Kianix must be running in Unity
def main():
    awake = True
    # while awake:
    try:
        kianix_awake()
    except:
        print("something went wrong, restarting")

if __name__ == '__main__':
    main()