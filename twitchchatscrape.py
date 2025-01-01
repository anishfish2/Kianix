import threading
import os
from dotenv import load_dotenv
import socket
import logging
from emoji import demojize
from datetime import datetime
import time
import subprocess
import sys
import redis

def restart_script():
    script_args = [sys.executable] + sys.argv
    subprocess.Popen(script_args)
    sys.exit()


def update_file(channel, redis_server):
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
        while True:
            try:

                resp = sock.recv(2048).decode('utf-8')
                if "ING: tmi.twitch.tv" in resp:
                    restart_script()
                username = ''.join(resp.split(" ")[0].split("!")[0].split("."))[1:] 
                message = resp.split(":")[-1]
                if message == "" or username == "tmitwitchtv" or "End of /NAMES list" in message:
                    continue
                if message.strip() == "tmi.twitch.tv":
                    restart_script()

                
                resp = username +": " + message
                print(resp)
                print("_____________________")
                if resp.startswith('PING'):
                    sock.send("PONG\n".encode('utf-8'))
                
                elif len(resp) > 0:
                    # redis_server.rpush('twitch_chat', resp)
                    continue
            except:
                continue

def write_data():
    # redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)

   # Key
    key = 'twitch_chat'

    # Check if the key exists and is a list
    # if not (redis_server.exists(key) and redis_server.type(key) == b'list'):
    #     redis_server.delete(key) 
    #     redis_server.lpush(key, '')

    while True:
        update_file("anishfish", None)


def main():
    write_data()
    
if __name__ == "__main__":
    main()