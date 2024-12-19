# This a honeypot wtih the time and data logger. The log is kept in the text file honeypot_log.txt. #


import socket
import threading
import time

# Log file to store connection attempts and messages
LOG_FILE = "honeypot_log.txt"
# Dictionary to store the last connection time for each IP
connection_times = {}

# Function to handle incoming connections
def handle_connection(client, addr):
    ip = addr[0]
    current_time = time.time()
    
    # Rate limiting: Allow only one connection per IP every 10 seconds
    if ip in connection_times and current_time - connection_times[ip] < 10:
        print(f"Rate limiting connection from {ip}")
        client.close()
        return
    
    connection_times[ip] = current_time
    
    print(f"Connection from {addr}")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Connection from {addr}\n")
    
    try:
        # Read data from the client (this is just for logging purposes)
        while True:
            data = client.recv(1024)
            if not data:
                break
            print(f"Received data: {data}")
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Received data from {addr}: {data}\n")
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        client.close()

# Main function to start the honeypot
def start_honeypot():
    host = "127.0.0.1"
    port = 2222
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)
    print(f"Honeypot listening on {host}:{port}")
    
    while True:
        try:
            client, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_connection, args=(client, addr)).start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == "__main__":
    start_honeypot()
