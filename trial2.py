import time
import os
import soundfile as sf
import numpy as np
import pygame
import scipy
os.environ['CURL_CA_BUNDLE'] = ''
from transformers import AutoProcessor, AutoModel

start_time = time.time()
processor = AutoProcessor.from_pretrained("suno/bark-small")
model = AutoModel.from_pretrained("suno/bark-small")

inputs = processor(
    text=["Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe."],
    return_tensors="pt",
)

# Generate speech values
speech_values = model.generate(**inputs, do_sample=True)
sampling_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav", rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())
end_time = time.time()
print("Elapsed time 1 is " + str(end_time - start_time))

pygame.mixer.init()
file_path = "bark_out.wav"
pygame.mixer.music.load(file_path)

pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
print("Elapsed time 2 is " + str(end_time - start_time))