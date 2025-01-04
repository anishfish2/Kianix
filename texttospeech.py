import soundfile as sf
import numpy as np
import sounddevice as sd
# import pyttsx3
import tkinter as tk
import win32api
import win32con
import pywintypes
import threading
from elevenlabs import set_api_key, generate, stream
# from dotenv import load_dotenv
import os 

def display_text(text, display_time):
    if len(text.split(' ')) > 30:
        font_size = 15
    else:
        font_size = 30
    def close_window():
        label.master.destroy()

    label = tk.Label(text=text, font=('Verdana', font_size), fg='black', bg='white', wraplength=400)
    label.master.overrideredirect(True)
    label.master.geometry("+250+250")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()

    # Get the screen width and height
    screen_width = label.master.winfo_screenwidth()
    screen_height = label.master.winfo_screenheight()

    # Calculate the coordinates to center the label on the left monitor
    label_width = label.winfo_reqwidth()
    label_height = label.winfo_reqheight()
    x_position = screen_width // 2 - label_width //3 * 6
    y_position = (screen_height - label_height) // 2

    # Set the label's position
    label.master.geometry(f"+{x_position}+{y_position}")

    # Close the window after the specified display time (in milliseconds)
    label.after(display_time, close_window)

    label.mainloop()

def playTTS(input_text, rate):
    load_dotenv()
    set_api_key(os.getenv('ELEVENLABS_API_KEY'))
    display_time = int(1/2 * len(input_text.split(" ")) * 1000)
    display_thread = threading.Thread(target=display_text, args=(input_text, display_time))
    display_thread.start()

    audio_stream = generate(
        text=input_text,
        voice="Kianix",
        model="eleven_monolingual_v1",
        stream=True)
    stream(audio_stream)
