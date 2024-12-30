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
        while True:
            try:

                resp = sock.recv(2048).decode('utf-8')
                if "ING: tmi.twitch.tv" in resp:
                    continue
                username = ''.join(resp.split(" ")[0].split("!")[0].split("."))[1:] 
                message = resp.split(":")[-1]
                if message == "" or username == "tmitwitchtv" or "End of /NAMES list" in message:
                    continue
                if message.strip() == "tmi.twitch.tv":
                    continue

                resp = username +": " + message
                print(resp)
                print("_____________________")
                if resp.startswith('PING'):
                    sock.send("PONG\n".encode('utf-8'))
                
                elif len(resp) > 0:
                    print(resp)
            except:
                continue

update_file("anishfish")
