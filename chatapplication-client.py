import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))  # Connect to the server
    print("Connected to the server. Type 'bye' to exit.")

    while True:
        message = input("You: ")
        client.send(message.encode())
        if message.lower() == "bye":
            print("Closing connection...")
            break
        reply = client.recv(1024).decode()
        if reply.lower() == "bye":
            print("Server has disconnected.")
            break
        print(f"Server: {reply}")

    client.close()

if __name__ == "__main__":
    start_client()
