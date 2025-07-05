import socket
import os
import threading
import json
from utils import hash_file

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 65433))

server.listen()
server.settimeout(1.0)

received_path = 'python_networking/file_transfer_app/received/'

try:
    while True:
        try:
            client, address = server.accept()
            
            metadata = b''
            while not metadata.endswith(b'\n'):
                chunk = client.recv(1)
                if not chunk:
                    break
                metadata += chunk
                
            print(metadata)
            
            metadata = json.loads(metadata.decode('utf-8').strip())
            
            print(metadata)
            
            file_size = metadata['file_size']
            file_name = metadata['file_name'].split('/')[-1]  + metadata['file_type']
            # name file is like "cyber_notes/3-7-2025.md" which makes error when trying to save it
            file_hash = metadata['hash']
            
            os.makedirs(os.path.join(received_path), exist_ok=True)
            
            received_bytes = 0
            
            with open(received_path + file_name, 'wb') as file:
                while True:
                    content = client.recv(1024)
                    if not content:
                        break # end of file reached
                    file.write(content)
                    received_bytes += len(content)
                print(f"Expected size: {metadata['file_size']} for {file_name}, Received: {received_bytes}")
            
            if received_bytes != file_size:
                print(f"File {file_name} was not received completely. Expected {file_size} bytes, but got {received_bytes} bytes.")
            else:
                print(f"File {file_name} received successfully.")
                if hash_file(os.path.join(received_path, file_name)) == file_hash:
                    print(f"File {file_name} hash matches the expected hash.")
                else:
                    print(f"File {file_name} hash does not match the expected hash. File may be corrupted.")
            client.close()
            
        except socket.timeout:
            continue # this line loops back and check for any Interrupt to break the application if needed
except KeyboardInterrupt:
    print("\nServer shutting down...")
    server.close()