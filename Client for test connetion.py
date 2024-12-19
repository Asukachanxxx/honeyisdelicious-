# Remember to run both windows openned. One with Client script running and the other with the Honeypot script#

import socket

def connect_to_server():
    # Define the server address and port
    server_address = ('127.0.0.1', 2222)
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        sock.connect(server_address)
        print(f"Connected to {server_address[0]} on port {server_address[1]}")
        
        # Keep the connection open for logging
        while True:
            data = sock.recv(1024)
            if data:
                print(f"Received: {data.decode('utf-8')}")
            else:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        sock.close()
        print("Connection closed")

if __name__ == "__main__":
    connect_to_server()
