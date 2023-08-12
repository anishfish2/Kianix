import threading
import os
from dotenv import load_dotenv
import socket
import logging
from emoji import demojize
from datetime import datetime
import time

def update_file(channel):

        load_dotenv()
        oauth = os.getenv('TWITCH_OAUTH')
        server = 'irc.chat.twitch.tv'
        port = 6667
        nickname = 'anishfish'
        token = oauth
        channel = "#" + channel
        sock = socket.socket()
        sock.connect((server, port))
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s — %(message)s',
                            datefmt='%Y-%m-%d_%H:%M:%S',
                            handlers=[logging.FileHandler("shared.txt", encoding='utf-8')])
        while True:
            resp = sock.recv(2048).decode('utf-8')
            username = ''.join(resp.split(" ")[0].split("!")[0].split("."))[1:] 
            message = resp.split(":")[-1]

            resp = username +": " + message

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            
            elif len(resp) > 0:
                logging.info(demojize(resp))

def write_data(write_event):
    while True:
        write_event.wait()  # Wait for the read to finish
        write_event.clear()  # Reset the event
        
        update_file("")

def main():
    write_event = threading.Event()
    writer_thread = threading.Thread(target=write_data, args=(write_event,))
    writer_thread.start()

    while True:
        input("Press Enter to read data from the file: ")

        write_event.clear()  # Pause the write operation
        read_data()
        write_event.set()  # Resume the write operation


def read_data():
    with open("shared.txt", "r") as file:
        data = file.read()
        print("Data read from the file:")
        print(data)

if __name__ == "__main__":
    main()
