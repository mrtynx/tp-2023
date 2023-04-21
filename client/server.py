import cv2
import socket
import pickle
import struct

BUF_SIZE = 4096


def main():
    # Configuration
    host = "127.0.0.1"
    port = 6666

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[*] Listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    while True:
        data_size_bytes = client_socket.recv(4)
        data_size = struct.unpack("!I", data_size_bytes)[0]

        data = b""
        while len(data) < data_size:
            remaining_data = data_size - len(data)
            chunk = client_socket.recv(min(remaining_data, BUF_SIZE))
            if not chunk:
                break
            data += chunk

        if len(data) != data_size:
            print("Error: Incomplete data received")
        else:
            print("Frame received")
            received = pickle.loads(data)
            cv2.imshow("transfer", received)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                server_socket.close()
                break


if __name__ == "__main__":
    main()
