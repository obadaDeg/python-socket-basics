import socket
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime

class ChatServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        self.clients = {}
        self.clients_lock = threading.Lock()
        self.server_socket = None
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Chat Server", font=("Arial", 16, "bold"), 
                              bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Server controls frame
        controls_frame = tk.Frame(self.root, bg='#2c3e50')
        controls_frame.pack(pady=5)
        
        # Port input
        port_frame = tk.Frame(controls_frame, bg='#2c3e50')
        port_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(port_frame, text="Port:", bg='#2c3e50', fg='#ecf0f1').pack(side=tk.LEFT)
        self.port_entry = tk.Entry(port_frame, width=8)
        self.port_entry.insert(0, "65433")
        self.port_entry.pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        self.start_btn = tk.Button(controls_frame, text="Start Server", 
                                  command=self.start_server, bg='#27ae60', fg='white',
                                  font=("Arial", 10, "bold"))
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(controls_frame, text="Stop Server", 
                                 command=self.stop_server, bg='#e74c3c', fg='white',
                                 font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Server: Stopped", 
                                    bg='#2c3e50', fg='#e74c3c', font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)
        
        # Connected clients frame
        clients_frame = tk.Frame(self.root, bg='#2c3e50')
        clients_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(clients_frame, text="Connected Clients:", bg='#2c3e50', 
                fg='#ecf0f1', font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.clients_listbox = tk.Listbox(clients_frame, height=4, bg='#34495e', 
                                         fg='#ecf0f1', selectbackground='#3498db')
        self.clients_listbox.pack(fill=tk.X, pady=5)
        
        # Log frame
        log_frame = tk.Frame(self.root, bg='#2c3e50')
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        tk.Label(log_frame, text="Server Log:", bg='#2c3e50', 
                fg='#ecf0f1', font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, bg='#34495e', 
                                                 fg='#ecf0f1', font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Clear log button
        clear_btn = tk.Button(self.root, text="Clear Log", command=self.clear_log,
                             bg='#95a5a6', fg='white')
        clear_btn.pack(pady=5)
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def update_clients_list(self):
        self.clients_listbox.delete(0, tk.END)
        with self.clients_lock:
            for nickname in self.clients.keys():
                self.clients_listbox.insert(tk.END, nickname)
                
    def broadcast(self, message):
        with self.clients_lock:
            disconnected_clients = []
            for nickname, client in self.clients.items():
                try:
                    client.sendall(message)
                except:
                    disconnected_clients.append(nickname)
            
            # Remove disconnected clients
            for nickname in disconnected_clients:
                del self.clients[nickname]
                self.root.after(0, self.update_clients_list)
                
    def handle_client(self, client_socket, nickname):
        welcome = f"{nickname} has joined the chat."
        self.broadcast(welcome.encode('utf-8'))
        self.root.after(0, lambda: self.log_message(welcome))
        self.root.after(0, self.update_clients_list)
        
        try:
            while self.is_running:
                message = client_socket.recv(1024)
                if not message:
                    break
                
                full_message = f"{nickname}: {message.decode('utf-8')}"
                self.root.after(0, lambda msg=full_message: self.log_message(msg))
                self.broadcast(full_message.encode('utf-8'))
        except:
            pass
        
        # Cleanup
        with self.clients_lock:
            if nickname in self.clients:
                del self.clients[nickname]
        client_socket.close()
        
        if self.is_running:
            goodbye = f"{nickname} has left the chat."
            self.broadcast(goodbye.encode('utf-8'))
            self.root.after(0, lambda: self.log_message(goodbye))
            self.root.after(0, self.update_clients_list)
            
    def accept_connections(self):
        while self.is_running:
            try:
                client_socket, addr = self.server_socket.accept()
                if not self.is_running:
                    client_socket.close()
                    break
                    
                nickname = client_socket.recv(1024).decode('utf-8')
                
                with self.clients_lock:
                    self.clients[nickname] = client_socket
                
                threading.Thread(target=self.handle_client, 
                               args=(client_socket, nickname), daemon=True).start()
                               
            except socket.error:
                if self.is_running:
                    self.root.after(0, lambda: self.log_message("Error accepting connection"))
                break
                
    def start_server(self):
        try:
            port = int(self.port_entry.get())
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('localhost', port))
            self.server_socket.listen()
            
            self.is_running = True
            self.log_message(f"Server started on port {port}")
            self.status_label.config(text=f"Server: Running on port {port}", fg='#27ae60')
            
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.DISABLED)
            
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"Failed to start server: {str(e)}")
            
    def stop_server(self):
        self.is_running = False
        
        # Close all client connections
        with self.clients_lock:
            for client in self.clients.values():
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            
        self.log_message("Server stopped")
        self.status_label.config(text="Server: Stopped", fg='#e74c3c')
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.NORMAL)
        
        self.update_clients_list()

def main():
    root = tk.Tk()
    app = ChatServerGUI(root)
    
    def on_closing():
        app.stop_server()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()