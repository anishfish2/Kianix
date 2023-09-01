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

def restart_script():
    script_args = [sys.executable] + sys.argv
    subprocess.Popen(script_args)
    sys.exit()


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

                if resp.startswith('PING'):
                    sock.send("PONG\n".encode('utf-8'))
                
                elif len(resp) > 0:
                    logging.info(demojize(resp))
            except:
                continue

def write_data(write_event):
    while True:
        write_event.wait()
        write_event.clear()
        update_file("forsen")


def main():
    file_path = "shared.txt"
    with open(file_path, "w") as file:
        pass

    write_event = threading.Event()
    writer_thread = threading.Thread(target=write_data, args=(write_event,))
    writer_thread.daemon = True  # Set the thread as daemon
    writer_thread.start()

    try:
        while True:
            input("Press Enter to read data from the file: ")
            write_event.clear()
            read_data()
            write_event.set()
    except KeyboardInterrupt:
        print("\nExiting the program...")
        write_event.set()  # Ensure that the writer thread can terminate
        writer_thread.join()  # Wait for the writer thread to finish
        sys.exit(0)


def read_data():
    with open("shared.txt", "r") as file:
        data = file.read()
        print(len(data))
        print("Data read from the file:")
        print(data)
        return data

if __name__ == "__main__":
    main()