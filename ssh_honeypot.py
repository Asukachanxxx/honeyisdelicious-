import socket
import sys
import threading
import paramiko
import datetime
import logging

# Configure logging
logging.basicConfig(
    filename='honeypot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SSHHoneypot(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username: str, password: str) -> int:
        # Log the attempted credentials
        logging.info(f"Login attempt - Username: {username} Password: {password}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username: str) -> str:
        return 'password'

def start_honeypot(port=2222):
    try:
        # Generate SSH key for the server
        host_key = paramiko.RSAKey.generate(2048)
        
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', port))
        sock.listen(100)
        
        print(f"[+] SSH Honeypot listening on port {port}")
        logging.info(f"Honeypot started on port {port}")

        while True:
            client, addr = sock.accept()
            print(f"[+] Connection from: {addr[0]}:{addr[1]}")
            logging.info(f"Connection from: {addr[0]}:{addr[1]}")

            try:
                # Set up SSH transport
                transport = paramiko.Transport(client)
                transport.add_server_key(host_key)
                ssh_honeypot = SSHHoneypot()
                
                transport.start_server(server=ssh_honeypot)
                
                # Wait for auth attempt
                channel = transport.accept(20)
                if channel is None:
                    transport.close()
                    continue

            except Exception as e:
                print(f"[-] Error: {str(e)}")
                logging.error(f"Error handling connection: {str(e)}")
                try:
                    transport.close()
                except:
                    pass

    except Exception as e:
        print(f"[-] Error: {str(e)}")
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_honeypot() 