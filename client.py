import socket
import speech_recognition as sr
from timeit import default_timer as timer
import asyncio

# 1. Setup socket connection with server

HOST = '10.32.80.163'  # Replace with server's IP address
PORT = 12345        # Same port as server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# 2. Keep listening to new audio
async def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5

        while True:
            print("Listening...")
            
            audio = recognizer.listen(source)
            await transcribe(recognizer, audio)

# Transcribe the audio
async def transcribe(recognizer, audio):
    try:
        start = timer()
        transcribed_words = recognizer.recognize_whisper(audio)
        end = timer()
        print("Time elapsed:", end - start)
        print("You said:", transcribed_words)
        print("=============")
        s.sendall(transcribed_words.encode("utf-8"))
    except sr.UnknownValueError:
        print("Whisper Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper Speech Recognition service; {0}".format(e))

asyncio.run(listen())