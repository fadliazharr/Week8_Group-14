import socket
import sys
import os

SERVER_ADDRESS = ('127.0.0.1', 5000)
CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
CLIENT_SOCKET.connect(SERVER_ADDRESS)

def system_interrupt():
    CLIENT_SOCKET.close()
    sys.exit(0)

BUF_SIZE = 1024

try:
    filename = input('Input filename to be sent: ')
    filesize = os.path.getsize(filename)
    CLIENT_SOCKET.send(str(filesize).encode())
    with open(filename, 'rb') as f:
        while True:
            try:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                CLIENT_SOCKET.send(data)
            except KeyboardInterrupt:
                system_interrupt()
        
    while True:
        try:
            percentage = float(CLIENT_SOCKET.recv(BUF_SIZE).decode())
            print(f"Server received {percentage}% of the file")
        except socket.timeout:
            print('Server is down') 
        else:
            break
        
except KeyboardInterrupt:
    system_interrupt()
