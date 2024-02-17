import speech_recognition as sr
from socket_client import send_message

init_rec = sr.Recognizer()
print("Let's speak!!")
with sr.Microphone() as source:
    audio_data = init_rec.record(source, duration=5)
    print("Recognizing your text...")
    text = init_rec.recognize_google(audio_data)

    send_message(text)