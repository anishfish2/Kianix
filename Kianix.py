from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import threading
import random

    

def kianix_awake(stop_event):
    askedQuestions = []

    time_awoken = time.time()

    currChat = read_data()
    numCurrentChatMessages = len(currChat.split('\n'))

    lastChatsRespondedTo = []
    plans = read_file('plans.txt')

    startStream(plans)
    while not stop_event.is_set():
        try:
            current_time = time.time()
            elapsed_time = current_time - time_awoken

            #currentAction = read_file("currentAction.txt")
            nothingUrgent = True
            if nothingUrgent:
                #If new chat
                currChat = read_data()
                newNumCurrentChatMessages = len(currChat.split('\n'))
                choice = random.randint(0, 10)
                if (newNumCurrentChatMessages != numCurrentChatMessages) and (choice <= 9):
                    numCurrentChatMessages = newNumCurrentChatMessages
                    twitchchatdata = currChat.split("\n")[-10:]
                    feed = ""
                    for i in twitchchatdata:
                        print(i)
                        if i not in lastChatsRespondedTo and i != "":
                            feed = i
                            print("User said: " + feed)
                            questionFromChat(feed)

                    if len(lastChatsRespondedTo) < 9:
                        lastChatsRespondedTo.append(feed)
                    else:
                        lastChatsRespondedTo = [feed]
                else:
                    decision = random.randint(0, 4)
                    if decision == 0:
                        print("questioning chat")
                        questionChat(askedQuestions)
                        
                        #Wait a bit
                        i = 0
                        while i < random.randint(50000000,100000000):
                            i+=1
                        # continue to next while loop, where check if response from chat has been generated
                        #continue

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
            print('died')
            print("Some Error Happened -> Restarting")
            continue

#Kianix must be running in Unity
def main():
    awake = True
    while awake:
        try:
            stop_event = threading.Event()

            # Create and start the threads
            loop_thread = threading.Thread(target=kianix_awake, args=(stop_event,))
            listener_thread = threading.Thread(target=key_listener, args=(stop_event,))

            loop_thread.start()
            listener_thread.start()

            # Wait for the loop thread to finish
            loop_thread.join()
            sayGoodbye()
            awake = False
        except:
            print("something went wrong, restarting")

if __name__ == '__main__':
    main()