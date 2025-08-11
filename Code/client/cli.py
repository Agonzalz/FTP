import socket
import sys

def main(server_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, port))
        greeting = sock.recv(1024).decode()
        print(greeting)        
        while True:
            command = input("ftp> ")
            if command.startswith("get") or command.startswith("put"):
                cmnd, filename = command.split()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_sock:
                    data_sock.bind((server_ip, 0))
                    port = data_sock.getsockname()[1]
                    command += f" {port}"
                    data_sock.listen(1)
                    sock.sendall(command.encode())
                    data_conn, address = data_sock.accept()
                    if command.startswith("get"):
                        with open(filename, 'wb') as file:
                            bytes_received = 0
                            while True:
                                data = data_conn.recv(4096)
                                if not data:
                                    break
                                file.write(data)
                                bytes_received += len(data)
                        print(f"{filename} downloaded, {bytes_received} bytes transferred")
                    elif command.startswith("put"):
                        with open(filename, 'rb') as file:
                            bytes_sent = 0
                            bytes_read = file.read(4096)
                            while bytes_read:
                                data_conn.sendall(bytes_read)
                                bytes_sent += len(bytes_read)
                                bytes_read = file.read(4096)
                        print(f"{filename} uploaded, {bytes_sent} bytes transferred")
                    data_conn.close()
            elif command == "quit":
                sock.sendall(command.encode())
                print(sock.recv(1024).decode())
                break
            else:
                sock.sendall(command.encode())
                response = sock.recv(4096).decode()
                print(response)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cli.py <SERVER_IP> <PORT>")
        sys.exit(1)
    main(sys.argv[1], int(sys.argv[2]))
