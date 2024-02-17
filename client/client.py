import socket
import subprocess
import speech_recognition as sr
from timeit import default_timer as timer
import asyncio
import os
from dotenv import load_dotenv
from client_agent_handler import handle_response

load_dotenv()
HOST = os.environ["HOST"]
PORT = int(os.environ["SERVER_LISTEN_PORT"])

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

# 2. Keep listening to new audio
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5
        try: 
            while True:
                print("Listening...")
                audio = recognizer.listen(source)
                transcribe(recognizer, audio)
        except KeyboardInterrupt:
            print("Notification receiving thread terminated.")


# Transcribe the audio
def transcribe(recognizer, audio):
    try:
        start = timer()
        transcribed_words = recognizer.recognize_whisper(audio)
        end = timer()
        print("Time elapsed:", end - start)
        print("You said:", transcribed_words)
        print("=============")
        socket.sendall(transcribed_words.encode("utf-8"))
        response = socket.recv(1024).decode('utf-8')
        print("HERE I AM TRYING TO RECEIVE DATA: " + response)
        if response != "No results":
            handle_response(response)
    except sr.UnknownValueError:
        print("Whisper Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper Speech Recognition service; {0}".format(e))
            
listen()