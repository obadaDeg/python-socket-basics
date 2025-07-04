import socket
import threading

clients = {}

def broadcast(message, sender_nickname):
    for nickname, client in clients.items():
        try:
            client.sendall(f"{sender_nickname}: {message.decode()}".encode('utf-8'))
        except:
            print(f"Could not send message to {nickname}. They may have disconnected.")

def handle_client(client_socket, nickname):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print(f"{nickname} has disconnected.")
                break
            
            print(f"{nickname}: {message.decode('utf-8')}")
            broadcast(message, nickname)
        except Exception as e:
            # print(f"Error with {nickname}: {e}")
            print(f"{nickname} has disconnected unexpectedly.")
            break
    
    client_socket.close()
    del clients[nickname]
    broadcast(f"{nickname} has left the chat.".encode('utf-8'), nickname)
    
def accept_connections(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        
        nickname = client_socket.recv(1024).decode('utf-8')
        clients[nickname] = client_socket
        print(f"{nickname} has joined the chat.")
        
        broadcast(f"{nickname} has joined the chat.".encode('utf-8'), nickname)
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, nickname))
        client_thread.start()
        
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65433))
    server_socket.listen(5)
    print("Server is listening on port 65433...")
    
    accept_thread = threading.Thread(target=accept_connections, args=(server_socket,))
    accept_thread.start()
    accept_thread.join()
    
if __name__ == "__main__":
    main()
    print("Server has stopped.")