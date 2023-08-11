import os
from dotenv import load_dotenv
import socket
import logging
from emoji import demojize
from datetime import datetime
import time
import multiprocessing
import re


file_path = 'chat_log.txt'
file_lock = multiprocessing.Lock()

def update_file():
    with file_lock:
        load_dotenv()
        oauth = os.getenv('TWITCH_OAUTH')
        server = 'irc.chat.twitch.tv'
        port = 6667
        nickname = 'anishfish'
        token = oauth
        channel = '#pokelawls'
        sock = socket.socket()
        sock.connect((server, port))
        sock.send(f"PASS {token}\n".encode('utf-8'))
        sock.send(f"NICK {nickname}\n".encode('utf-8'))
        sock.send(f"JOIN {channel}\n".encode('utf-8'))

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s — %(message)s',
                            datefmt='%Y-%m-%d_%H:%M:%S',
                            handlers=[logging.FileHandler('chat_log.txt', encoding='utf-8')])
        while True:
            resp = sock.recv(2048).decode('utf-8')
            #print(resp)
            username = ''.join(resp.split(" ")[0].split("!")[0].split("."))[1:] 
            message = resp.split(":")[-1]
            # save = username + ":" + message

            resp = username +": " + message

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            
            elif len(resp) > 0:
                logging.info(demojize(resp))

            


def main():
    try:
        update_file()
    except Exception as e:
        print("Locked chat file", e)


if __name__ == "__main__":
    main()



