# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai
audio_file= open("C:/Users/Owner/Desktop/Projects/Kianix/temp.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)