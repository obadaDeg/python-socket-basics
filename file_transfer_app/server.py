import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 65433))

server.listen()
server.settimeout(1.0)

try:
    while True:
        try:
            client, address = server.accept()
        except socket.timeout:
            continue
except KeyboardInterrupt:
    print("\nServer shutting down...")
    server.close()