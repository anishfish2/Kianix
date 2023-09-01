import speech_recognition as sr

def listen_for_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for speech...")
        audio = recognizer.listen(source, timeout=None)  # Continuously listen until speech stops
        
        try:
            print("Transcribing speech...")
            text = recognizer.recognize_google(audio)  # Use Google Web Speech API for transcription
            return text
        except sr.UnknownValueError:
            print("Speech not understood")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return None

if __name__ == "__main__":
    while True:
        speech = listen_for_speech()
        if speech:
            print("Transcribed Text:", speech)