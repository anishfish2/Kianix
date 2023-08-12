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

    numCurrentChatMessages = len(read_data().split('\n'))

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
                newNumCurrentChatMessages = len(read_data().split('\n'))
                choice = random.randint(1, 10)
                if (newNumCurrentChatMessages != numCurrentChatMessages) and (choice < 9):
                    numCurrentChatMessages = newNumCurrentChatMessages
                    twitchchatdata = read_data().split("\n")[-10:]
                    feed = ""
                    for i in twitchchatdata:
                        if len(i.split(" ")) > 6:
                            feed = i
                    if feed not in lastChatsRespondedTo:
                        print("User said: " + feed)
                        questionFromChat(feed)

                    if len(lastChatsRespondedTo) < 9:
                        lastChatsRespondedTo.append(feed)
                    else:
                        lastChatsRespondedTo = [feed]
                else:
                    decision = random.randint(0, 4)
                    if decision == 0:
                        questionChat(askedQuestions)
                        
                        #Wait a bit
                        i = 0
                        while i < random.randint(50000000,100000000):
                            i+=1
                        # continue to next while loop, where check if response from chat has been generated
                        #continue

                    elif decision == 3:
                        generateConversation()
                    
                    elif decision == 4:
                        generateJoke()

                    elif decision == 5:
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