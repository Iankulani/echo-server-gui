import tkinter as tk
from tkinter import messagebox
import socket

def print_error_and_exit(message):
    messagebox.showerror("Error", message)
    root.quit()  # Exits the main event loop

def send_message():
    # Get user input from the GUI
    server_ip = entry_ip.get()
    try:
        server_port = int(entry_port.get())
    except ValueError:
        print_error_and_exit("Invalid port number. Please enter a valid integer for the port.")
        return
    message = entry_message.get()

    # Create a socket
    try:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print_error_and_exit(f"Error creating socket: {e}")
        return

    # Set up the server address
    server_addr = (server_ip, server_port)

    # Connect to the server
    try:
        sockfd.connect(server_addr)
    except socket.error as e:
        print_error_and_exit(f"Connection to the server failed: {e}")
        return

    # Send the message to the server
    try:
        sockfd.sendall(message.encode())
    except socket.error as e:
        print_error_and_exit(f"Error sending data to server: {e}")
        return

    # Receive the echoed message from the server
    try:
        data = sockfd.recv(1024)
        if not data:
            messagebox.showinfo("Server Response", "Server closed the connection.")
        else:
            messagebox.showinfo("Server Response", f"Received echoed message from server: {data.decode()}")
    except socket.error as e:
        print_error_and_exit(f"Error receiving data from server: {e}")
    
    # Close the socket
    sockfd.close()

# Create the main window
root = tk.Tk()
root.title("TCP Client")

# Create the layout for the GUI
tk.Label(root, text="Enter the server IP address:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_ip = tk.Entry(root)
entry_ip.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter the server port number:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_port = tk.Entry(root)
entry_port.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Enter the message to send to the server:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_message = tk.Entry(root)
entry_message.grid(row=2, column=1, padx=10, pady=5)

# Create a button to send the message
send_button = tk.Button(root, text="Send Message", command=send_message)
send_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()
