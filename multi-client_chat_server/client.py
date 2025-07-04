import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                print("Disconnected from server.")
                break
            print(message.decode('utf-8'))
        except:
            print("Error receiving message from server.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65433))

    nickname = input("Enter your nickname: ")
    client.sendall(nickname.encode('utf-8'))

    # Start receiver thread
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    # Send messages
    while True:
        message = input("Type a message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        client.sendall(message.encode('utf-8'))

    client.close()
    print("Connection closed. Goodbye!")

if __name__ == "__main__":
    main()
