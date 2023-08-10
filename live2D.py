import socket
import time

# Kianix must be running in Unity

def send_data(identifier, data):
    
    if identifier == "AnimationTrigger":
        send = ""
        if data == "curious":
            send = "curioustrigger"
        elif data == "thinking":
            send = "thinkingtrigger"
        elif data == "uneasy":
            send = "neutraltrigger"
        elif data == "shocked":
            send = "absentmindedtrigger"
        elif data == "pleased":
            send = "cutetrigger"
        elif data == "surprised":
            send = "surprisetrigger"
        elif data == "happy":
            send = "happytrigger"
        elif data == "amazed":
            send = "smiletrigger"
        elif data == "sorrow":
            send = "sorrowtrigger"
    elif identifier == "Expression":
        send=""
        if data.lower() == "stars()":
            send = "0"
        elif data.lower() == "hearts()":
            send = "3"
        elif data.lower() == " cry()":
            send = "1"
        elif data.lower() == "turnoffsigil()":
            send = "2"
        elif data.lower() == "default()":
            send = "5"
        elif data.lower() == "blureyes()":
            send = "6"
        elif data.lower() == "powerstate()":
            send = "7"
        elif data.lower() == "noflowers()":
            send = "4"

    send = f"{identifier}:{send}"
    HOST = 'localhost'
    PORT = 12345  # Choose a free port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(send.encode())
    except:
        print("sending data failed: " + send)

def send_animation_trigger(trigger_name):
    send_data("AnimationTrigger", trigger_name)

def send_expression(expression):
    send_data("Expression", expression)

