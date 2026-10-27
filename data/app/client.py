import socket

# 1. Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect to the server's IP and Port
try:
    client_socket.connect(('127.0.0.1', 5555))
    
    # 3. Send a message
    message = "Hello Server! I am the Client."
    client_socket.send(message.encode('utf-8'))
    
    # 4. Receive the reply
    reply = client_socket.recv(1024).decode('utf-8')
    print(f"Server replied: {reply}")

except ConnectionRefusedError:
    print("Could not connect. Is the server running?")

finally:
    # 5. Close the socket
    client_socket.close()