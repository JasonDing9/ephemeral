import socket

HOST = '10.32.82.125'  # Replace with your server's IP address
PORT = 12345        # Choose an available port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f'Received: {data.decode("utf-8")}')