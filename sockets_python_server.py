# sockets_python_server.py
# This is a simple TCP server that listens for incoming connections, receives messages from clients,
# and sends back a response. It will continue to run until manually stopped or until a client
# sends the message 'exit'.


# One-Message-Per-Connection (stateless) server example using Python's socket library

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 65432))
server.listen()

print("Server is listening...")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    data = conn.recv(1024)
    if not data:
        break

    message = data.decode('utf-8')
    print(f"Received: {message}")

    response = "Hello, Client! Your message was received."
    conn.sendall(response.encode('utf-8'))

    conn.close()  # Close after serving the client

# this server handles one message per connection and then closes the connection.
# so if you tried to send multiple messages from the client, you will get this 
# Traceback (most recent call last):
#   File "C:\Users\obada\Desktop\testing\python_code\python_networking\sockets_python_client.py", line 16, in <module>
#     response = client.recv(1024)
# ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine

# Uncomment the following code to run a Persistent Connection (stateful) server example

# Persistent Connection (stateful) server example using Python's socket library
# import socket

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('localhost', 65432))
# server.listen()

# print("Server is listening...")

# while True:
#     conn, addr = server.accept()
#     print(f"Connected by {addr}")
    
#     while True:
#         data = conn.recv(1024)
#         if not data:
#             break  # Client disconnected

#         message = data.decode('utf-8')
#         print(f"Received: {message}")

#         if message.lower() == 'exit':
#             break

#         response = "Hello, Client! Your message was received."
#         conn.sendall(response.encode('utf-8'))

#     conn.close()
#     print(f"Connection with {addr} closed.")
