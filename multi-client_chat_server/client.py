import socket
import threading
import sys

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                print("\nDisconnected from server.")
                break

            sys.stdout.write(f"\r{message.decode('utf-8')}\n> ")
            sys.stdout.flush()
        except:
            print("\nError receiving message. Connection closed.")
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 65433))

    nickname = input("Enter your nickname: ")
    client.sendall(nickname.encode('utf-8'))

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        message = input("> ")
        if message.lower() == 'exit':
            break
        client.sendall(message.encode('utf-8'))

    client.close()
    print("Connection closed. Goodbye!")

if __name__ == "__main__":
    main()
