# sockets_python_server.py
# ----------------------------------------
# This is a simple TCP server program.
# It listens for one client at a time.
# When a client connects, it talks to them in a loop:
# receiving messages and sending back a reply.
# If the client says 'exit' or disconnects, it closes the connection.
# This is a stateful server, meaning it can talk to a client multiple times before closing.
# ----------------------------------------

import socket  # Import the socket library to use networking features

# Step 1: Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Step 2: Bind the socket to localhost (your own computer) and port 65432
# bind means "listen here for incoming connections"
server.bind(('localhost', 65432))

# Step 3: Start listening for incoming connections
server.listen()
print("Server is ready and waiting for connections on port 65432...")

# Step 4: Run the server forever
while True:
    # Accept a new client connection
    conn, addr = server.accept()  # conn = connection object, addr = client address
    print(f"Client connected from {addr}")

    # Step 5: Talk to the client in a loop
    while True:
        # Wait to receive data from the client
        data = conn.recv(1024)  # Receives up to 1024 bytes
        if not data:
            # If no data is received, the client has disconnected
            print("Client disconnected unexpectedly.")
            break

        # Decode the message from bytes to string
        message = data.decode('utf-8')
        print(f"Client says: {message}")

        # If the client says 'exit', stop the conversation
        if message.lower() == 'exit':
            print("Client ended the conversation.")
            break

        # Send a response back to the client
        response = "Hello, I received your message!"
        conn.sendall(response.encode('utf-8'))

    # Step 6: Close the connection to this client
    conn.close()
    print(f"Connection with {addr} closed.\n")
