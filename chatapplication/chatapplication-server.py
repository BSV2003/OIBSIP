import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5000))  # Server address and port
    server.listen(1)
    print("Server started. Waiting for a connection...")
    
    conn, addr = server.accept()
    print(f"Connection established with {addr}")

    while True:
        message = conn.recv(1024).decode()
        if message.lower() == "bye":
            print("Client has disconnected.")
            break
        print(f"Client: {message}")
        reply = input("You: ")
        conn.send(reply.encode())
        if reply.lower() == "bye":
            print("Closing connection...")
            break

    conn.close()

if __name__ == "__main__":
    start_server()
