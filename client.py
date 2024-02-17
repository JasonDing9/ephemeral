import socket
import speech_recognition as sr

# 1. Setup socket connection with server

HOST = '10.32.80.163'  # Replace with server's IP address
PORT = 12345        # Same port as server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# 2. Keep listening to new audio

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    recognizer.adjust_for_ambient_noise(source)

    while True:
        audio = recognizer.listen(source)
        try:
            transcribed_words = recognizer.recognize_google(audio)
            print("You said:", transcribed_words)
            s.sendall(transcribed_words.encode("utf-8"))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
