import socket
import subprocess
import speech_recognition as sr
from timeit import default_timer as timer
import asyncio
import os

HOST = os.environ["HOST"]
PORT = os.environ["SERVER_SEND_PORT"]


