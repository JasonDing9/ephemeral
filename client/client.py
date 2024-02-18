import socket
import speech_recognition as sr
from timeit import default_timer as timer
import time
import os
import threading
from dotenv import load_dotenv
from client_agent_handler import handle_response

load_dotenv()
NAME = os.environ['NAME']
HOST = os.environ["HOST"]
PORT = int(os.environ["SERVER_LISTEN_PORT"])

action_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
action_socket.connect((HOST, PORT))

# 2. Keep listening to new audio
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5
        
        recognizer.energy_threshold = 1000
        # recognizer.dynamic_energy_threshold = True
        # recognizer.dynamic_energy_adjustment_damping = 0.15
        # recognizer.dynamic_energy_adjustment_ratio = 2.5
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
        if len(transcribed_words) < 3:
            print("Blank audio")
            return
        transcribed_words = f"{NAME} said: {transcribed_words}"
        print("Time elapsed:", end - start)
        print(transcribed_words)
        print("=============")
        action_socket.sendall(transcribed_words.encode("utf-8"))
        response = action_socket.recv(1000000).decode('utf-8')
        if not response:
            return
        print("Data Received: " + response)
        if response != "No results" or response != None:
            handle_response(response)
    except sr.UnknownValueError:
        print("Whisper Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper Speech Recognition service; {0}".format(e))
            

def start_client_process():
    listen()
start_client_process()