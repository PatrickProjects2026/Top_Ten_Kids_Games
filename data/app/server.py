import socket

# 1. Create a socket (AF_INET = IPv4, SOCK_STREAM = TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind the socket to an address and port
# Port 5555 is usually free for testing
server_socket.bind(('127.0.0.1', 5555))

# 3. Listen for incoming connections
server_socket.listen(1)
print("Server is started. Waiting for a player to connect...")

# 4. Accept a connection
connection, address = server_socket.accept()
print(f"Connected to: {address}")

# 5. Receive data (1024 bytes max)
data = connection.recv(1024).decode('utf-8')
print(f"Client sent: {data}")

# 6. Send a response back
connection.send("Message received! Hello from the Server.".encode('utf-8'))

# 7. Close the connection
connection.close()
server_socket.close()