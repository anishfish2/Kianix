from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import threading
import random

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
def kianix_awake(stop_event):
    askedQuestions = []

    #read the latest twitchemssage
    
    while not stop_event.is_set():
        try:
            #Can't end stream if its on respond to chat
            prevStatement = ""
            decision = random.randint(2,2)
            if decision == 0:
                print("Chat question:")
                respondToChat()
            elif decision == 1:
                print("Asking chat a question:")
                questionChat(askedQuestions)
            elif decision == 2:
                twitchchatdata = read_data().split("\n")[-10:]
                for i in twitchchatdata:
                    if len(i.split(" ")) > 6:
                        feed = i
                print("User said this: " +  feed)
                questionFromChat(feed)
            elif decision == 3:
                print("Generating Conversation:")
                generateConversation()
            elif decision == 4:
                print("Generating Joke:")
                generateJoke()
            elif decision == 5:
                print("Generating SelfTalk:")
                generateSelfTalk()
            elif decision == 6:
                emote()
        except:
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