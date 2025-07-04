import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from datetime import datetime


class ChatClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("500x600")
        self.root.configure(bg="#2c3e50")

        self.client_socket = None
        self.connected = False
        self.nickname = ""

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Chat Client",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        title_label.pack(pady=10)

        # Connection frame
        conn_frame = tk.Frame(self.root, bg="#2c3e50")
        conn_frame.pack(pady=5)

        # Server input
        server_frame = tk.Frame(conn_frame, bg="#2c3e50")
        server_frame.pack(side=tk.LEFT, padx=5)

        tk.Label(server_frame, text="Server:", bg="#2c3e50", fg="#ecf0f1").pack(
            side=tk.LEFT
        )
        self.server_entry = tk.Entry(server_frame, width=12)
        self.server_entry.insert(0, "localhost")
        self.server_entry.pack(side=tk.LEFT, padx=2)

        # Port input
        port_frame = tk.Frame(conn_frame, bg="#2c3e50")
        port_frame.pack(side=tk.LEFT, padx=5)

        tk.Label(port_frame, text="Port:", bg="#2c3e50", fg="#ecf0f1").pack(
            side=tk.LEFT
        )
        self.port_entry = tk.Entry(port_frame, width=8)
        self.port_entry.insert(0, "65433")
        self.port_entry.pack(side=tk.LEFT, padx=2)

        # Connect button
        self.connect_btn = tk.Button(
            conn_frame,
            text="Connect",
            command=self.connect_to_server,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        # Disconnect button
        self.disconnect_btn = tk.Button(
            conn_frame,
            text="Disconnect",
            command=self.disconnect_from_server,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED,
        )
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Status: Disconnected",
            bg="#2c3e50",
            fg="#e74c3c",
            font=("Arial", 10, "bold"),
        )
        self.status_label.pack(pady=5)

        # Chat display frame
        chat_frame = tk.Frame(self.root, bg="#2c3e50")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        tk.Label(
            chat_frame,
            text="Chat Messages:",
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Arial", 12, "bold"),
        ).pack(anchor=tk.W)

        self.chat_text = scrolledtext.ScrolledText(
            chat_frame,
            bg="#34495e",
            fg="#ecf0f1",
            font=("Consolas", 10),
            state=tk.DISABLED,
        )
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Message input frame
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(
            input_frame,
            text="Message:",
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Arial", 10, "bold"),
        ).pack(anchor=tk.W)

        message_frame = tk.Frame(input_frame, bg="#2c3e50")
        message_frame.pack(fill=tk.X, pady=5)

        self.message_entry = tk.Entry(
            message_frame, font=("Arial", 10), state=tk.DISABLED
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(
            message_frame,
            text="Send",
            command=self.send_message,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED,
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # Clear chat button
        clear_btn = tk.Button(
            self.root,
            text="Clear Chat",
            command=self.clear_chat,
            bg="#95a5a6",
            fg="white",
        )
        clear_btn.pack(pady=5)

    def display_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, formatted_message)
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def clear_chat(self):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024)
                if not message:
                    break

                self.root.after(
                    0, lambda msg=message.decode("utf-8"): self.display_message(msg)
                )
            except:
                break

        if self.connected:
            self.root.after(0, self.handle_disconnection)

    def handle_disconnection(self):
        self.display_message("Disconnected from server.")
        self.connected = False
        self.status_label.config(text="Status: Disconnected", fg="#e74c3c")

        # Update UI
        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.server_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        self.message_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)

        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

    def connect_to_server(self):
        # Get nickname
        nickname = simpledialog.askstring(
            "Nickname", "Enter your nickname:", parent=self.root
        )
        if not nickname:
            return

        try:
            server = self.server_entry.get()
            port = int(self.port_entry.get())

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server, port))

            # Send nickname
            self.client_socket.sendall(nickname.encode("utf-8"))

            self.connected = True
            self.nickname = nickname

            self.display_message(f"Connected to {server}:{port} as {nickname}")
            self.status_label.config(
                text=f"Status: Connected as {nickname}", fg="#27ae60"
            )

            # Update UI
            self.connect_btn.config(state=tk.DISABLED)
            self.disconnect_btn.config(state=tk.NORMAL)
            self.server_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            self.message_entry.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL)

            # Focus on message entry
            self.message_entry.focus_set()

            # Start receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None

    def disconnect_from_server(self):
        if self.connected:
            self.connected = False
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None

            self.display_message("Disconnected from server.")
            self.status_label.config(text="Status: Disconnected", fg="#e74c3c")

            # Update UI
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.server_entry.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.NORMAL)
            self.message_entry.config(state=tk.DISABLED)
            self.send_btn.config(state=tk.DISABLED)

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message and self.connected:
            try:
                self.client_socket.sendall(message.encode("utf-8"))
                self.message_entry.delete(0, tk.END)
            except:
                self.handle_disconnection()
                messagebox.showerror(
                    "Error", "Failed to send message. Connection lost."
                )


def main():
    root = tk.Tk()
    app = ChatClientGUI(root)

    def on_closing():
        app.disconnect_from_server()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
