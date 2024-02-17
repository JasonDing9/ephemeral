import socket
import subprocess
import speech_recognition as sr
from timeit import default_timer as timer
import asyncio
import os

HOST = os.environ["HOST"]
PORT = os.environ["SERVER_LISTEN_PORT"]

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# # 2. Keep listening to new audio
# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         # recognizer.adjust_for_ambient_noise(source)
#         recognizer.pause_threshold = 0.5

#         while True:
#             print("Listening...")
            
#             audio = recognizer.listen(source)
#             transcribe(recognizer, audio)

# # Transcribe the audio
# def transcribe(recognizer, audio):
#     try:
#         start = timer()
#         transcribed_words = recognizer.recognize_whisper(audio)
#         end = timer()
#         print("Time elapsed:", end - start)
#         print("You said:", transcribed_words)
#         print("=============")
#         s.sendall(transcribed_words.encode("utf-8"))
#     except sr.UnknownValueError:
#         print("Whisper Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Whisper Speech Recognition service; {0}".format(e))

# def receive_nofication():
#     while True:
#         data = s.recv(1024)
#         script = data.decode("utf-8")
#         try: 
#             subprocess.run(["osascript", "-e", script])
#         except Exception as e:
#             print(e)
            
# # asyncio.run(listen())
# transcription_thread = threading.Thread(target=listen, args=())
# transcription_thread.start()
# receive_notif_thread = threading.Thread(target=receive_nofication, args=())
# receive_notif_thread.start()

# Create a lock for socket operations
socket_lock = threading.Lock()

def listen(recognizer, source, socket):
    try:
        while True:
            print("Listening...")
            audio = recognizer.listen(source)
            transcribe(recognizer, audio, socket)
    except KeyboardInterrupt:
        print("Listening thread terminated.")

def transcribe(recognizer, audio, socket):
    try:
        start = timer()
        transcribed_words = recognizer.recognize_whisper(audio)
        end = timer()
        print("Time elapsed:", end - start)
        print("You said:", transcribed_words)
        print("=============")
        with socket_lock:
            socket.sendall(transcribed_words.encode("utf-8"))
    except sr.UnknownValueError:
        print("Whisper Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper Speech Recognition service; {0}".format(e))

def receive_notification(socket):
    try:
        while True:
            with socket_lock:
                data = socket.recv(1024)
            script = data.decode("utf-8")
            try:
                subprocess.run(["osascript", "-e", script])
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        print("Notification receiving thread terminated.")

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.5

        # Create a socket
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.connect((HOST, 12345))

        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receive_socket.connect((HOST, 12345))

        # socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.connect((HOST, 12345))

        # Start listening and notification threads
        transcription_thread = threading.Thread(target=listen, args=(recognizer, source, listen_socket))
        receive_notif_thread = threading.Thread(target=receive_notification, args=(receive_socket,))

        transcription_thread.start()
        receive_notif_thread.start()

        try:
            # Keep the main thread running
            transcription_thread.join()
            receive_notif_thread.join()
        except KeyboardInterrupt:
            print("Main thread terminated.")
            # socket.close()
            listen_socket.close()  # Close the socket when terminating the program
            receive_socket.close()  # Close the socket when terminating the program
