import soundfile as sf
import numpy as np
import sounddevice as sd
import pyttsx3
import sys

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

def generate_audio_from_text(text, voice_name):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set the desired voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == voice_name:
            engine.setProperty('voice', voice.id)
            break

    # Generate audio from text
    engine.save_to_file(text, 'temp.wav')
    engine.runAndWait()

def playTTS(input_text):
    # Number of semitones to shift the pitch
    semitones_to_shift = 2  # You can adjust this value as needed

    # Voice name (you may need to find the appropriate voice name for your system)
    desired_voice_name = "Microsoft Zira Desktop - English (United States)"

    # Generate audio from text using the desired voice
    generate_audio_from_text(input_text, desired_voice_name)

    # Load the generated audio using soundfile
    generated_audio, sample_rate = sf.read('temp.wav')

    # Apply pitch modification
    modified_audio = change_pitch(generated_audio, semitones_to_shift)

    # Play the modified audio using sounddevice
    sd.play(modified_audio, sample_rate)
    sd.wait()

    print("Pitch modification and audio playback complete.")
