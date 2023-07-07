import tkinter as tk
import cv2
import os
from PIL import Image, ImageTk
import subprocess
from threading import Thread


class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam App")
        self.root.attributes('-fullscreen', True)  # Open tkinter window in full screen

        # Add a heading label
        self.heading_label = tk.Label(root, text="Face Recognition", font=("Arial", 20, "bold"))
        self.heading_label.pack(pady=10)

        # Create a frame to hold the video label
        self.video_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        self.video_frame.pack(pady=10)

        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

        # Create a frame to hold the buttons and close button
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.capture_button = tk.Button(self.button_frame, text="Capture Image", command=self.capture_image)
        self.capture_button.grid(row=0, column=0, padx=10)

        self.execute_script1_button = tk.Button(self.button_frame, text="Execute Script 1", command=self.execute_script1)
        self.execute_script1_button.grid(row=0, column=1, padx=10)

        self.execute_script2_button = tk.Button(self.button_frame, text="Execute Script 2", command=self.execute_script2)
        self.execute_script2_button.grid(row=0, column=2, padx=10)

        self.close_button = tk.Button(self.button_frame, text="Close", command=self.close_app)
        self.close_button.grid(row=0, column=3, padx=10)

        # Create a frame to hold the directory input
        self.directory_frame = tk.Frame(root)
        self.directory_frame.pack(pady=10)

        self.directory_label = tk.Label(self.directory_frame, text="Enter Directory Name:")
        self.directory_label.grid(row=0, column=0)

        self.directory_entry = tk.Entry(self.directory_frame, width=30)
        self.directory_entry.grid(row=0, column=1, padx=10)

        self.directory_button = tk.Button(self.directory_frame, text="Start", command=self.start_webcam)
        self.directory_button.grid(row=0, column=2)

        self.camera = None
        self.image_counter = 1
        self.image_directory = ""
        self.script1_running = False

    def start_webcam(self):
        self.image_directory = self.directory_entry.get().strip()
        if not self.image_directory:
            tk.messagebox.showwarning("Invalid Directory", "Please enter a valid directory name.")
            return

        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)

        self.directory_button.configure(state=tk.DISABLED)
        self.capture_button.configure(state=tk.NORMAL)
        self.directory_entry.configure(state=tk.DISABLED)

        self.camera = cv2.VideoCapture(0)
        self.update_video()

    def update_video(self):
        _, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)

        self.video_label.config(image=photo)
        self.video_label.image = photo

        if self.camera.isOpened():
            self.root.after(10, self.update_video)
        else:
            self.capture_button.configure(state=tk.DISABLED)
            self.directory_button.configure(state=tk.NORMAL)
            self.directory_entry.configure(state=tk.NORMAL)

    def capture_image(self):
        _, frame = self.camera.read()
        image_path = os.path.join(self.image_directory, f"captured_image_{self.image_counter}.jpg")
        cv2.imwrite(image_path, frame)
        self.image_counter += 1

        if self.image_counter > 10:
            self.camera.release()
            self.directory_button.configure(state=tk.NORMAL)

            # Remove the video frame from the GUI after capturing images
            self.video_frame.pack_forget()

            # Add code here to perform any post-processing or analysis on the captured images

    def execute_script1(self):
        if not self.script1_running:
            self.script1_running = True
            script_path = "script1.py"
            thread = Thread(target=self.execute_script, args=(script_path,))
            thread.start()

    def execute_script(self, script_path):
        self.execute_script1_button.configure(state=tk.DISABLED)
        self.execute_script2_button.configure(state=tk.DISABLED)
        self.directory_button.configure(state=tk.DISABLED)
        self.close_button.configure(state=tk.DISABLED)

        loader_label = tk.Label(self.button_frame, text="Loading...", font=("Arial", 14, "bold"))
        loader_label.grid(row=0, column=4, padx=10)

        subprocess.call(["python", script_path])

        self.execute_script1_button.configure(state=tk.NORMAL)
        self.execute_script2_button.configure(state=tk.NORMAL)
        self.directory_button.configure(state=tk.NORMAL)
        self.close_button.configure(state=tk.NORMAL)

        loader_label.grid_forget()
        self.script1_running = False

    def execute_script2(self):
        if not self.script1_running and self.execute_script1_button["state"] == tk.NORMAL:
            script_path = "script2.py"
            subprocess.call(["python", script_path])
            self.root.destroy()

    def close_app(self):
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("800x600")
    app = WebcamApp(root)
    root.mainloop()
