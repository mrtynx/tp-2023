# Python program to open the
# camera in Tkinter
# Import the libraries,
# tkinter, cv2, Image and ImageTk


import cv2
import tkinter as tk
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window_title="Webcam App"):
        self.window = tk.Tk()
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)
        self.window.geometry("720x512")

        # Attrs
        self.server_ip = None
        self.server_port = None

        # Video
        self.label = tk.Label()
        self.label.pack()
        self.label.place(x=0, y=0)
        self.video_capture = cv2.VideoCapture(0)

        # Ip addr label
        self.ip_label = tk.Label(text="Enter server address")
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

        # Button
        self.btn = tk.Button(text="Send to server", command=self.print_msg, width=13)
        self.btn.place(x=540, y=125)

        self.update_frame()

        self.window.mainloop()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = cv2.resize(frame, (512, 512))
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label.photo_image = photo
            self.label.configure(image=photo)

        self.window.after(10, self.update_frame)

    def get_ip(self, event):
        self.server_ip = self.ip_entry.get()

    def get_port(self, event):
        self.server_port = self.port_entry.get()

    def print_msg(self, *args):
        print(f"ip = {self.server_ip}, port = {self.server_port}")

    def close_app(self):
        self.video_capture.release()
        self.window.destroy()


if __name__ == "__main__":
    app = WebcamApp()
