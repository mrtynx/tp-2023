import cv2
import socket
import io
import tkinter as tk
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window_title="Webcam to Docker IMG sender"):
        self.window = tk.Tk()
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.geometry("690x512")

        # Attrs
        self.buf_sz = 40960000
        self.server_ip = "127.0.0.1"
        self.server_port = 6666
        self.socket = None
        self.sock_connected = False
        self.cap = True
        self.snapshot_img = None

        # Video
        self.label = tk.Label()
        self.label.pack()
        self.label.place(x=0, y=0)
        self.video_capture = cv2.VideoCapture(0)

        # Ip addr label
        self.ip_label = tk.Label(text="Enter server IP")
        self.ip_label.pack()
        self.ip_label.place(x=540, y=0)

        # Ip addr entry
        self.ip_entry = tk.Entry(width=16)
        self.ip_entry.pack()
        self.ip_entry.place(x=540, y=30)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.bind("<Return>", self.get_ip)

        # Port label
        self.ip_label = tk.Label(text="Enter server port")
        self.ip_label.pack()
        self.ip_label.place(x=540, y=60)

        # Port entry
        self.port_entry = tk.Entry(width=16)
        self.port_entry.pack()
        self.port_entry.place(x=540, y=90)
        self.port_entry.insert(0, "6969")
        self.port_entry.bind("<Return>", self.get_port)

        # Connect button
        self.btn = tk.Button(
            text="Connect to server", command=self.connect_to_socket, width=13
        )
        self.btn.place(x=540, y=125)

        # Snapshot button
        self.snapshot_btn = tk.Button(text="Snapshot", width=13, command=self.snapshot)
        self.snapshot_btn.place(x=540, y=400)

        # Resume button
        self.resume_btn = tk.Button(
            text="Resume vid", width=13, command=self.resume_video
        )
        self.resume_btn.place(x=540, y=430)

        # Send button
        self.send_btn = tk.Button(text="Send", width=13, command=self.send_image)
        self.send_btn.place(x=540, y=460)

        self.update_frame()

        self.window.mainloop()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (512, 512))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            # if self.cap:
            self.snapshot_img = frame
            self.label.photo_image = photo
            self.label.configure(image=photo)

        self.window.after(10, self.update_frame)

        if self.sock_connected:
            self.send_image()

    def get_ip(self, event):
        self.server_ip = self.ip_entry.get()

    def get_port(self, event):
        self.server_port = int(self.port_entry.get())

    def connect_to_socket(self, *args):
        if self.server_port is not None or self.server_ip is not None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.sock_connected = True
            print(f"[*] Connected to {self.server_ip}:{self.server_port}")
        else:
            print("Enter full server information")

    def snapshot(self, *args):
        self.cap = False

    def resume_video(self, *args):
        self.cap = True

    def send_image(self, *args):
        if self.sock_connected:
            img = Image.fromarray(self.snapshot_img)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="JPEG")
            img_data = img_bytes.getvalue()
            img_stream = io.BytesIO(img_data)
            data = img_stream.read(self.buf_sz)
            while data:
                self.socket.send(data)
                data = img_stream.read(self.buf_sz)
        else:
            print("Cannot send image because socket not connected")

    def close_app(self):
        if self.socket is not None:
            self.socket.close()
        self.video_capture.release()
        self.window.destroy()


if __name__ == "__main__":
    app = WebcamApp()
