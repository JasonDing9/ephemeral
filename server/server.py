import socket
import threading
import sys
import os
from dotenv import load_dotenv
from classifier import classify
from actions.suggestions import get_suggestions

load_dotenv()

action_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = os.environ["HOST"]
PORT = int(os.environ["SERVER_LISTEN_PORT"])

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SEND_HOST = os.environ["HOST"]
SEND_PORT = int(os.environ["SERVER_SEND_PORT"])

FILE = open("actions/central-log.txt", "w")
FILE.seek(0)
FILE.truncate()
FILE.close()

def handle_client(client_socket):
    # This function will handle the communication with each client
    while True:
        file = open("actions/central-log.txt", "a")
        
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # Break the loop if no data is received
        print(f"Received data from {client_socket.getpeername()}: {data.decode('utf-8')}")
        data = data.decode('utf-8')
        print(f"Write? {data.find(':')} + 2 < {len(data)}")
        if (data.find(":") + 2 < len(data)):
            file.write(data + "\n")
        json_result = classify(data)
        # file.write(data)
        if json_result:
            client_socket.sendall(json_result.encode('utf-8'))
        else: 
            client_socket.sendall("No results".encode('utf-8'))
            
        file.close()
    # Close the connection when the client disconnects
    print(f"Connection with {client_socket.getpeername()} closed.")
    file.close()
    client_socket.close()

def start_server():
    # Bind the socket to a specific address and port
    server_address = (HOST, PORT)
    action_socket.bind(server_address)
    send_server_address = (SEND_HOST, SEND_PORT)
    send_socket.bind(send_server_address)

    # Listen for incoming connections (maximum 5 clients in the queue)
    action_socket.listen(5)
    send_socket.listen()
    print("Listening server is listening for incoming connections...")

    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = action_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Create a new thread to handle the communication with the client
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

            send_client_socket, send_client_address = send_socket.accept()
            print(f"Accepted send connection from {send_client_address}")

            send_client_handler = threading.Thread(target=send_insights, args=(send_client_socket,))
            send_client_handler.start()
        
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Shutting down the server.")
        shutdown_server()

def send_insights(send_client_socket):
    while True:
        data = send_client_socket.recv(1024)
        if not data:
            break
        
        results = get_suggestions()
        print("-========START========-")
        print("Results: " + results)
        print("-=========END=========-")
        send_client_socket.sendall(results.encode('utf-8'))

def shutdown_server():
    print("Shutting down the listening server.")
    FILE.close()
    sys.exit(0)

start_server()