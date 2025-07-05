import socket
import os
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 65433))

server.listen()
server.settimeout(1.0)

received_path = 'python_networking/file_transfer_app/received/'

try:
    while True:
        try:
            client, address = server.accept()
            os.makedirs(os.path.join(received_path), exist_ok=True)
            with open(received_path + "file.md", 'wb') as file:
                while True:
                    content = client.recv(1024)
                    file.write(content)
                    if not content:
                        break # end of file reached
            
        except socket.timeout:
            continue # this line loops back and check for any Interrupt to break the application if needed
except KeyboardInterrupt:
    print("\nServer shutting down...")
    server.close()