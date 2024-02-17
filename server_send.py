import classifier
import socket
import threading
import sys
import os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = os.environ["HOST"]
PORT = os.environ["SERVER_SEND_PORT"]