import socket
import keyboard
import time

def send_animation_trigger(trigger_name):
    HOST = 'localhost'
    PORT = 12345  # Choose a free port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(trigger_name.encode())
        time.sleep(1)
        # Call this line to set the animation trigger
        # s.sendall(b"SetAnimationToTrigger(disapointedtrigger)")  # Change the trigger name accordingly
        #s.sendall(string_data.encode('utf-8'))