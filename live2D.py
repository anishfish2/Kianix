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
        if data.lower() == "donothing()":
            send = "0"
        elif data.lower() == "confused()":
            send = "1"
        elif data.lower() == "hearts()":
            send = "2"
        elif data.lower() == "angry()":
            send = "3"
        elif data.lower() == "pentablet()":
            send = "7"
        elif data.lower() == "noheadband()":
            send = "8"
        elif data.lower() == "blush()":
            send = "9"
        elif data.lower() == "blankeyes()":
            send = "11"
        elif data.lower() == "pout()":
            send = "12"
        elif data.lower() == "writetablet()":
            send = "14"
        elif data.lower() == "brighteyes()":
            send = "15"
    send = f"{identifier}:{send}"
    HOST = 'localhost'
    PORT = 12345  # Choose a free port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("sending" + send)
            s.connect((HOST, PORT))
            s.sendall(send.encode())
    except:
        print("sending data failed: " + send)

def send_animation_trigger(trigger_name):
    send_data("AnimationTrigger", trigger_name)

def send_expression(expression):
    send_data("Expression", expression)

