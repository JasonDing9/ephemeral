import socket
import speech_recognition as sr
from timeit import default_timer as timer
import time
import os
import threading
from dotenv import load_dotenv
from client_agent_handler import handle_response

load_dotenv()

SEND_HOST = os.environ["HOST"]
SEND_PORT = int(os.environ["SERVER_SEND_PORT"])

ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ping_socket.connect((SEND_HOST, SEND_PORT))

def ping_for_insights():
    try: 
        while True:
            print("Pinging for insights...")
            ping_socket.sendall("I want insights!".encode('utf-8'))
            insight = ping_socket.recv(4096)
            print("Insight:", insight)
            handle_response(insight)
            if not insight:
                break
            time.sleep(10)
    except KeyboardInterrupt:
        return

def start_client_process():
    ping_for_insights()

start_client_process()