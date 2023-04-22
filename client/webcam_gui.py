import pickle
import socket
import struct
import tkinter as tk

import cv2
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window_title="Object detection inference client"):
        self.window = tk.Tk()
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.geometry("800x640")
        self.framerate = 100
        self.window.config(bg="#3B4252")
        self.x = 655
        self.y = 535

        # Properties
        self.server_ip = "127.0.0.1"
        self.server_port = 6666
        self.socket = None
        self.sock_connected = False
        self.detect = False
        self.snapshot_img = None

        # Video
        self.canvas = tk.Label(
            width=640,
            height=640,
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.place(x=0, y=0)
        self.video_capture = cv2.VideoCapture(0)

        # Ip addr entry
        self.ip_entry = tk.Entry(
            width=15,
            bg="#4C566A",
            bd=0,
            highlightthickness=0,
            relief="flat",
            fg="white",
        )
        self.ip_entry.pack()
        self.ip_entry.place(x=self.x, y=self.y)
        self.ip_entry.insert(0, "localhost")
        self.ip_entry.bind("<FocusOut>", self.get_ip)
        self.ip_entry.bind("<Button-1>", self.ip_onclick)

        # Port entry
        self.port_entry = tk.Entry(
            width=15,
            bg="#4C566A",
            bd=0,
            highlightthickness=0,
            relief="flat",
            fg="white",
        )
        self.port_entry.pack()
        self.port_entry.place(x=self.x, y=self.y + 30)
        self.port_entry.insert(0, "6969")
        self.port_entry.bind("<FocusOut>", self.get_port)
        self.port_entry.bind("<Button-1>", self.port_onclick)

        # Connect button
        self.connect_btn = tk.Button(
            text="Connect",
            command=self.connect_to_socket,
            width=12,
            bd=0,
            fg="white",
            highlightthickness=0,
            relief="flat",
            anchor="center",
            justify="center",
        )
        self.connect_btn.place(x=self.x, y=self.y + 60)
        self.connect_btn.config(bg="#5E81AC")

        # Detect button
        self.detect_btn = tk.Button(
            text="Detect",
            command=self.start_detection,
            width=12,
            bd=0,
            fg="white",
            highlightthickness=0,
            relief="flat",
            anchor="center",
            justify="center",
        )
        self.detect_btn.place(x=self.x, y=250)
        self.detect_btn.config(bg="#A3BE8C")

        # Stop button
        self.stop_btn = tk.Button(
            text="Stop",
            command=self.stop_detection,
            width=12,
            bd=0,
            fg="white",
            highlightthickness=0,
            relief="flat",
            anchor="center",
            justify="center",
        )
        self.stop_btn.place(x=self.x, y=285)
        self.stop_btn.config(bg="#BF616A")

        self.update_frame()

        self.window.mainloop()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 640))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            # if self.cap:
            self.snapshot_img = frame
            self.canvas.photo_image = photo
            self.canvas.configure(image=photo)

        self.window.after(self.framerate, self.update_frame)

        if self.sock_connected and self.detect:
            self.send_frame()
            msg = self.socket.recvmsg(1024)
            print(msg)

    def ip_onclick(self, event):
        self.ip_entry.delete(0, tk.END)

    def port_onclick(self, event):
        self.port_entry.delete(0, tk.END)

    def get_ip(self, event):
        self.server_ip = self.ip_entry.get()

    def get_port(self, event):
        try:
            self.server_port = int(self.port_entry.get())
        except:
            print("Invalid port entry")

    def start_detection(self, *args):
        self.detect = True

    def stop_detection(self, *args):
        self.detect = False

    def connect_to_socket(self, *args):
        if self.server_port is not None or self.server_ip is not None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.sock_connected = True
            print(f"[*] Connected to {self.server_ip}:{self.server_port}")
        else:
            print("Enter full server information")

    def send_frame(self, *args):
        if self.sock_connected:
            # img = cv2.cvtColor(self.snapshot_img, cv2.COLOR_BGR2GRAY)
            data = pickle.dumps(self.snapshot_img)
            # print(f"Sending {len(data)} bytes")
            data_size_bytes = struct.pack("!I", len(data))
            self.socket.sendall(data_size_bytes)
            self.socket.sendall(data)
        else:
            print("Cannot send image because socket not connected")

    def close_app(self):
        if self.socket is not None:
            self.socket.close()
        self.video_capture.release()
        self.window.destroy()


if __name__ == "__main__":
    app = WebcamApp()
