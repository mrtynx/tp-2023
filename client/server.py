import socket
from PIL import Image


BUF_SIZE = 40960000


def main():
    # Configuration
    host = "127.0.0.1"
    port = 6666

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[*] Listening on {host}:{port}")

    # Accept client connection
    while True:
        client_socket, client_address = server_socket.accept()
        while True:
            data = client_socket.recv(BUF_SIZE)
            if data:
                print("Frame received")
                img = open("img.jpg", "wb")
                img.write(data)
                img.close()
                data = None
                continue


if __name__ == "__main__":
    main()
