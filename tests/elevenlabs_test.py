from elevenlabs import set_api_key, generate, stream
import requests

from dotenv import load_dotenv
import os

load_dotenv()
set_api_key(os.getenv('ELEVENLABS_API_KEY'))

def text_stream():
    yield "Hi there, I'm Eleven "
    yield "I'm a text to speech API "

audio_stream = generate(
    text=text_stream(),
    voice="Kianix",
    model="eleven_monolingual_v1",
    stream=True
)

stream(audio_stream)