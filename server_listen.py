import classifier
import socket
import threading
import sys
import os

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = os.environ["HOST"]
PORT = os.environ["SERVER_LISTEN_PORT"]
FILE = open("central-log.txt", "a")

def handle_client(client_socket):
    # This function will handle the communication with each client
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # Break the loop if no data is received
        print(f"Received data from {client_socket.getpeername()}: {data.decode('utf-8')}")
        data = data.decode('utf-8')
        # classifier(data)
        FILE.write(data + "\n")
    # Close the connection when the client disconnects
    print(f"Connection with {client_socket.getpeername()} closed.")
    client_socket.close()

def start_server():
    # Bind the socket to a specific address and port
    server_address = (HOST, PORT)
    socket.bind(server_address)

    # Listen for incoming connections (maximum 5 clients in the queue)
    socket.listen(5)
    print("Listening server is listening for incoming connections...")

    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = socket.accept()
            print(f"Accepted connection from {client_address}")

            # Create a new thread to handle the communication with the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Shutting down the server.")
        shutdown_server()

def shutdown_server(signum=None, frame=None):
    print("Shutting down the listening server.")
    FILE.close()
    sys.exit(0)

start_server()