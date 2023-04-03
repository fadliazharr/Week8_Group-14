import socket 
import sys
import os

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(server_address)

def system_interrupt():
    client_socket.close()
    sys.exit(0)

buf = 1024

try:
    filename = input('Input filename to be sent: ')
    filesize = os.path.getsize(filename)
    client_socket.send(str(filesize).encode())
    
    with open(filename, 'rb') as f:
        block = 0
        while True:
            try:
                ack = False
                data = f.read(1024)
                if not data:
                    print('Finished sending data')
                    break
                block += 1
                
                while not ack:
                    client_socket.send(str(block).encode())
                    client_socket.send(data)
                    ack_server = client_socket.recv(1024).decode()
                    print(ack_server, end='\r')
                    if 'ack' in ack_server:
                        ack = True
                
            except KeyboardInterrupt:
                system_interrupt()
        
    while True:
        try:
            percentage = float(client_socket.recv(1024).decode())
            print(f'Server received {percentage}% of the file')
        except socket.timeout:
            print('Server is down') 
        else:
            break
        
except KeyboardInterrupt:
    system_interrupt()
