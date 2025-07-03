# this is a simple TCP client that connects to a server, sends messages, and receives responses.
# It will continue to send messages until the user types 'exit'.
# This client is designed to work with the server code provided above.
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65432))

while True:
    message = input("Enter a message to send to the server (or 'exit'): ")
    client.sendall(message.encode('utf-8'))

    if message.lower() == 'exit':
        break

    response = client.recv(1024)
    print(f"Received: {response.decode('utf-8')}")

client.close()
