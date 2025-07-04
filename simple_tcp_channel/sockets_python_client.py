# sockets_python_client.py
# ----------------------------------------
# This is a simple TCP client program.
# It connects to a server on your own machine (localhost)
# and lets you send messages repeatedly.
# After you send a message, it waits for the server to reply.
# You can type 'exit' to end the conversation and close the app.
# ----------------------------------------

import socket  # Import Python’s built-in networking library

# Step 1: Create a socket (like a phone you use to talk to the server)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Connect to the server at localhost, port 65432
client.connect(('localhost', 65432))

# Step 3: Keep sending messages until the user types 'exit'
while True:
    message = input("Type a message to send (or 'exit' to quit): ")

    # Send the message to the server (must be in bytes)
    client.sendall(message.encode('utf-8'))

    # If the message was 'exit', break out of the loop
    if message.lower() == 'exit':
        break

    # Wait for the server to send a response
    response = client.recv(1024)  # Receives up to 1024 bytes
    print(f"Server replied: {response.decode('utf-8')}")

# Step 4: Close the socket (hang up the phone)
client.close()
print("Connection closed. Goodbye!")
