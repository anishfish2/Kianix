import soundfile as sf
import numpy as np
import sounddevice as sd
import pyttsx3
import tkinter as tk
import win32api
import win32con
import pywintypes
import threading
def change_pitch(data, semitones):
    # Calculate the pitch shift factor
    pitch_shift = 2 ** (semitones / 12.0)

    # Apply pitch shift using resampling
    shifted_data = np.interp(
        np.arange(0, len(data), pitch_shift),
        np.arange(0, len(data)),
        data
    )

    return shifted_data

def generate_audio_from_text(text, voice_name, rate):
    #Initialize the TTS engine
    engine = pyttsx3.init()

    # Set the desired voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == voice_name:
            engine.setProperty('voice', voice.id)
            break

    # Set the speaking rate (speech speed)
    engine.setProperty('rate', rate)

    # Generate audio from text
    engine.save_to_file(text, 'temp.wav')
    engine.runAndWait()

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
    display_time = int(1/2 * len(input_text.split(" ")) * 1000)
    display_thread = threading.Thread(target=display_text, args=(input_text, display_time))
    display_thread.start()

    # Number of semitones to shift the pitch
    semitones_to_shift = 2  # You can adjust this value as needed

    # Voice name (you may need to find the appropriate voice name for your system)
    desired_voice_name = "Microsoft Zira Desktop - English (United States)"

    # Speaking rate (words per minute)
    desired_speaking_rate = 120  # Adjust the rate as needed

    # Generate audio from text using the desired voice and speaking rate
    generate_audio_from_text(input_text, desired_voice_name, desired_speaking_rate)

    # Load the generated audio using soundfile
    generated_audio, sample_rate = sf.read('temp.wav')

    # Apply pitch modification
    modified_audio = change_pitch(generated_audio, semitones_to_shift)

    # Play the modified audio using sounddevice
    sd.play(modified_audio, sample_rate)
    sd.wait()

#playTTS( "This is a long text that will wrap automatically within the label to fit the specified wraplength.", 120)