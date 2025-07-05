import socket
import cryptography
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65433))

file_path = 'cyber_notes/3-7-2025.md'

os.path.getsize(filename=file_path)


with open(file_path, 'rb') as file:
    # print(file.read())

    client.sendfile(file)

