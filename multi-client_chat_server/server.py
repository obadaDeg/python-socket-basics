import socket
import threading

clients = {}
clients_lock = threading.Lock()

def broadcast(message):
    with clients_lock:
        for client in clients.values():
            try:
                client.sendall(message)
            except:
                print(f"Failed to send message to a client. It may have disconnected.")
                pass

def handle_client(client_socket, nickname):
    welcome = f"{nickname} has joined the chat.\n".encode('utf-8')
    broadcast(welcome)
    print(welcome.decode().strip())

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break  # Client disconnected

            full_message = f"{nickname}: {message.decode('utf-8')}".encode('utf-8')
            print(full_message.decode())
            broadcast(full_message)
    except:
        print(f"{nickname} has disconnected unexpectedly.")

    # Cleanup
    with clients_lock:
        del clients[nickname]
    client_socket.close()
    goodbye = f"{nickname} has left the chat.\n".encode('utf-8')
    broadcast(goodbye)
    print(goodbye.decode().strip())

def accept_connections(server_socket):
    while True:
        client_socket, _ = server_socket.accept()
        nickname = client_socket.recv(1024).decode('utf-8')

        with clients_lock:
            clients[nickname] = client_socket

        threading.Thread(target=handle_client, args=(client_socket, nickname), daemon=True).start()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65433))
    server_socket.listen()
    print("Server is listening on port 65433...")

    accept_connections(server_socket)

if __name__ == "__main__":
    main()
