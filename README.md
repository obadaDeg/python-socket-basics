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

# 💬 Multi-Client Chat App (Terminal-Based)

A simple Python-based chat server and client that supports multiple users communicating over TCP sockets using threads. Messages are broadcast to all clients, and each user sees messages from others in real-time.

---

## 📸 Screenshot

![Chat Screenshot](multi-client_chat_server/docs/chat_screenshot.png)

> 📌 Place your terminal screenshot inside the `docs/` folder and rename it to `chat_screenshot.png`.

---

## 🚀 Features

- Multi-client support using threading
- Real-time message broadcasting
- Proper handling of client join/leave events
- Clean input/output handling with no prompt overlap
- Simple terminal-based interface

---

## 📁 Project Structure

