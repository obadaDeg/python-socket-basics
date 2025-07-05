import socket
import hashlib
import os
from utils import hash_file
import json


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65433))

file_path = 'cyber_notes/3-7-2025.md'

metadata = {}

metadata['file_size'] = os.path.getsize(file_path)
file_name, file_type = os.path.splitext(file_path)
metadata['file_name'] = file_name
metadata['file_type'] = file_type
metadata['hash'] = hash_file(file_path)

print(metadata)

client.sendall((json.dumps(metadata) + '\n').encode())


with open(file_path, 'rb') as file:
    # print(file.read())

    client.sendfile(file)

