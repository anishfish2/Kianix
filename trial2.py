from full_query import full_query
from insert_memory import insert_memory
from dotenv import load_dotenv
import random
import time
from kianix_functions import *
import threading
import random
from twitchchatscrape import * 

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

    #read the latest twitchemssage
    print("got here")
    twitchchatdata = read_data().split("\n")[0]
    print(twitchchatdata)

    print("User said this: " +  twitchchatdata)
    questionFromChat(twitchchatdata)
          

#Kianix must be running in Unity
def main():
    awake = True
    try:
        stop_event = threading.Event()

        # Create and start the threads
        loop_thread = threading.Thread(target=kianix_awake, args=(stop_event,))
        listener_thread = threading.Thread(target=key_listener, args=(stop_event,))

        loop_thread.start()
        listener_thread.start()

        # Wait for the loop thread to finish
        loop_thread.join()
        awake = False
    except:
        print("something went wrong, restarting")

if __name__ == '__main__':
    main()