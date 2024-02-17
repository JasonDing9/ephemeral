import socket

HOST = '10.32.82.125'  # Replace with server's IP address
PORT = 12345        # Same port as server

def send_message(message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode("utf-8"))