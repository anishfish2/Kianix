import socket
import requests
import os
import firebase_admin
from firebase_admin import firestore
import time
import datetime

client_id = os.getenv('TWITCH_CLIENT_ID') 
access_token = os.getenv('TWITCH_OAUTH')
channel_name = 'anishfish'


print(client_id, access_token)
server = 'irc.chat.twitch.tv'
port = 6667

oauth_token = f'oauth:{access_token}'

def connect_to_irc():
    print("Connecting to Twitch IRC server...")
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    print(f"Connected to {server} on port {port}.")
    
    return irc

def join_channel(irc):
    irc.send(f'PASS {oauth_token}\r\n'.encode('utf-8'))
    irc.send(f'NICK anishfish\r\n'.encode('utf-8')) 
    irc.send(f'JOIN #{channel_name}\r\n'.encode('utf-8'))  

def read_chat(irc):
    app = firebase_admin.initialize_app(options={'projectId' :'kianix'})
    db = firestore.client(app)
    while True:
        response = irc.recv(2048).decode('utf-8')
        if response.startswith('PING'):
            irc.send('PONG :' + response.split()[1] + '\r\n'.encode('utf-8')) 
            print("Responding to PING.")
        elif 'PRIVMSG' in response:
            user = response.split('!')[0][1:]  
            message = response.split('PRIVMSG')[1].split(':', 1)[1]  
            chat = db.collection("streamers").document("Kianix")
            
            doc = chat.get()
            if doc.exists:
                data = doc.to_dict()
                chat_log = data.get('chat_log', [])
                
                new_chat_entry = {
                    'message': message,
                    'user': user,
                    'timestamp': datetime.datetime.utcnow()  
                }
                
                chat_log.append(new_chat_entry)
                
                chat.update({
                    'chat_log': chat_log
                })

            print(f"{user}: {message}")


def main():
    try:
        irc = connect_to_irc()
        join_channel(irc)
        read_chat(irc)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
