# Python Socket Basics

This repository contains simple examples demonstrating how to use Python's built-in `socket` library to implement basic TCP client-server communication.

## 📄 Files

- `sockets_python_client.py`  
  A TCP client that connects to a server, sends user input, and displays responses. Ends when 'exit' is typed.

- `sockets_python_server.py`  
  A TCP server that handles client connections. Includes both:
  - **Stateless (One message per connection)** mode
  - **Persistent (Multiple messages per connection)** mode (commented for optional use)

## 🚀 How to Run

1. Start the server:
   ```bash
   python sockets_python_server.py


# NOTE
This is a starter repository intended for learning and experimentation. You might find it a bit messy at times as it's actively evolving. Improvements and cleanups will follow as the project progresses.