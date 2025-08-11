import socket
import sys
import subprocess

def data_channel(data_sock, filename, command):
    try:
        if command == 'get':
            with open(filename, 'rb') as file:
                bytes_read = file.read(4096)
                while bytes_read:
                    data_sock.sendall(bytes_read)
                    bytes_read = file.read(4096)
            print(f"SUCCESS: Sent '{filename}'")
        elif command == 'put':
            with open(filename, 'wb') as file:
                bytes_read = data_sock.recv(4096)
                while bytes_read:
                    file.write(bytes_read)
                    bytes_read = data_sock.recv(4096)
            print(f"SUCCESS: Received '{filename}'")
    except FileNotFoundError:
        print(f"FAILURE: File '{filename}' not found")
        data_sock.sendall(b'Error: File not found')
    except Exception as e:
        print(f"FAILURE: {str(e)}")
        data_sock.sendall(f'Error: {str(e)}'.encode())
    finally:
        print(f"data channel closing on port {data_sock.getsockname()[1]}")
        data_sock.close()

def control_channel(conn):
    while True:
        command = conn.recv(1024).decode().strip()
        if not command:
            break

        if command == "quit":
            conn.sendall(b"Goodbye")
            break

        cmd, *args = command.split()
        if cmd == "ls":
            try:
                result = subprocess.check_output(["ls"])
                lines = result.decode("utf-8").splitlines()
                ls = "File list: \n"
                for string in lines :
                    ls += string + "\n"
                conn.sendall(ls.encode())
                print(f"SUCCESS: Listed files for directory")
            except Exception as e:
                conn.sendall(f"FAILURE: {str(e)}".encode())
                print(f"FAILURE: {str(e)}")
        elif cmd in ["get", "put"]:
            filename = args[0]
            data_port = int(args[1])
            data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                data_sock.connect(('localhost', data_port))
                print(f"Connected to data channel through ephemeral port {data_port}")
                data_channel(data_sock, filename, cmd)
            except Exception as e:
                print(f"FAILURE: Could not connect to data port {data_port}: {str(e)}")

    conn.close()
    #print(f"Connection closed with {addr}")
    print(f"Connection closed with")


def main(port):
    host = '0.0.0.0'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server started on {host}:{port}. Waiting for connections...")
    while True:
        conn, addr = server_socket.accept()
        conn.sendall(f"You are now connected to {host}\n Type commands (ls, get <filename>, put <filename>, quit).".encode())
        print(f"Connected by {addr}")
        control_channel(conn)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pythonserv.py <PORT>")
        sys.exit(1)
    main(int(sys.argv[1]))
