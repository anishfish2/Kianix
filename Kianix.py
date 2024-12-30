from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import random
import redis
    

def kianix_awake():
    askedQuestions = []

    time_awoken = time.time()
    
    redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    plans = read_plans(redis_server)

    startStream(plans)
    
    stream_on = True

    while stream_on:
        try:
            print('Waking up')
            current_time = time.time()
            elapsed_time = current_time - time_awoken

            nothingUrgent = True
            prevChat = None
            print("got here")
            if nothingUrgent:
                print("GOt here 1")
                #If new chat
                currChat = read_chat(redis_server)
                print("yo")
                choice = random.randint(0, 10)
                # time.sleep(random(1, 5))
                print("GOt here 2")
                if choice <= 9 and currChat != "" and currChat != " " and currChat != None and currChat != prevChat:
                    print("User said: " + currChat + ". I am responding!")
                    questionFromChat(currChat)
                else:
                    decision = random.randint(0, 6)
                    if decision == 0:
                        print("Questioning chat")
                        askedQuestions += questionChat(askedQuestions)
                        
                    elif decision == 3:
                        print("Making conversation")
                        generateConversation()
                    
                    elif decision == 4:
                        print("Generating a joke")
                        generateJoke()

                    elif decision == 5:
                        print("Talking to myself")
                        generateSelfTalk()

                    elif decision == 6:
                        print("Commenting on the game")
                        comment_game()
                print("ending action cycle")
                prevChat = currChat
                print("GOt here 3")
        except:
            print("Error in kianix_awake -> Restarting")

#Kianix must be running in Unity
def main():
    awake = True
    while awake:
        try:
            kianix_awake()
        except:
            sayGoodbye()
            break

if __name__ == '__main__':
    main()