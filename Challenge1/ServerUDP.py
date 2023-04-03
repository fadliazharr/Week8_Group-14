import socket
import sys
import os

SERVER_ADDRESS = ('127.0.0.1', 5000)
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind(SERVER_ADDRESS)

def server_interrupt():
    print('Server is interrupted')
    SERVER_SOCKET.close()
    sys.exit(0)

filename_start = 'receivedfile_'
file_count = 0
          
while True:
    try:
        file_count += 1
        filename = f"{filename_start}{file_count}.txt"
        
        SERVER_SOCKET.settimeout(None)
        while True:
            try:
                data, client_address = SERVER_SOCKET.recvfrom(1024)
                if data:
                    break  
            except KeyboardInterrupt:
                server_interrupt()
                
        actual_filesize = int(data.decode())
        
        SERVER_SOCKET.settimeout(5)
        with open(filename, 'wb') as f:
            while True:
                try:
                    data = SERVER_SOCKET.recv(1024)
                    if not data:
                        break
                except socket.timeout:
                    break
                except KeyboardInterrupt:
                    server_interrupt()
                else:
                    f.write(data)
            
        received_filesize = os.path.getsize(filename)
        percentage = (received_filesize / actual_filesize) * 100
        print('')
        print(f"Finished receiving from {client_address} from socket {SERVER_SOCKET.getsockname()}")
        print(f"Received {percentage}% of the file from sender.")
        SERVER_SOCKET.sendto(str(percentage).encode(), client_address)
        
    except KeyboardInterrupt:
        server_interrupt()
