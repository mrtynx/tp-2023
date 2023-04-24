import socket
import cv2
from PIL import Image
import numpy as np


def main():
    # Configuration
    host = "127.0.0.1"
    port = 12345
    buffer_size = 4096

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(30)
    print(f"[*] Listening on {host}:{port}")

    # Accept client connection
    conn, addr = server_socket.accept()
    print(f"[*] Connection established with {addr}")

    # Receive and display images
    while True:
        # Receive image data from socket
        img_data = b""
        while True:
            chunk = conn.recv(buffer_size)
            if not chunk:
                break
            img_data += chunk

        # Convert image data to NumPy array and display image
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        cv2.imwrite("obrzaok.jpg", img)
        print("Image saved")

    # Clean up
    conn.close()


if __name__ == "__main__":
    main()
