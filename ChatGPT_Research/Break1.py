import tkinter as tk
from tkinter import messagebox
import csv
import webbrowser
import cv2
from PIL import Image, ImageTk
from Page7 import Page7

class Break1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.font_style = ("Helvetica", 24)
        self.setup_ui()

    def setup_ui(self):
        self.breakLabel = tk.Label(self, text="Time for a 2 Minute Break", font=self.font_style)
        self.breakLabel.grid(row=0, column=1, pady=20)

        self.label = tk.Label(self, text="00:02:00", font=self.font_style)  # 2:00
        self.label.grid(row=1, column=1, pady=20)

        self.start_button = tk.Button(self, text="Start Break", command=self.start_break)
        self.start_button.grid(row=2, column=1, pady=20)

        self.next_page_button = tk.Button(self, text="Next Page", command=self.go_to_next_page)
        self.next_page_button.grid(row=3, column=1, pady=20)
        self.next_page_button.config(state="disabled")  # Initially disable the button

        # Label to display video frames
        self.video_label = tk.Label(self)
        self.video_label.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

    def on_show_frame(self):
        self.tkraise()  # Raise this frame to the top when shown

    def start_break(self):
        self.start_timer(120)  # 120 seconds
        self.open_youtube_video()
        self.setup_camera()
        self.start_button.config(state="disabled")  # Disable the start button once clicked

    def start_timer(self, t=10):
        mins, secs = divmod(t, 60)
        self.label.config(text=f"{mins:02d}:{secs:02d}")
        if t > 0:
            self.after(1000, self.start_timer, t-1)
        else:
            self.label.config(text="Time's up! Move to the Next Page", fg="red")
            self.next_page_button.config(state="normal")  # Enable the button when the timer ends

    def open_youtube_video(self):
        # URL of the YouTube video to open
        url = "https://www.youtube.com/watch?v=u_m94hysna4"  # Replace with your desired video URL
        webbrowser.open(url)

    def setup_camera(self):
        """Set up the camera and start recording."""
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('break_recording_1.avi', fourcc, 20.0, (640, 480))
        self.update_video()

    def update_video(self):
        """Capture frame from the webcam and update the label every 10 ms."""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)
                frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_LINEAR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk
            self.after(10, self.update_video)

    def go_to_next_page(self):
        # Stop recording and release resources
        self.on_hide()
        self.controller.show_page(Page7)

    def on_hide(self):
        """Release camera and video writer resources."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.out and self.out.isOpened():
            self.out.release()
            self.out = None
        self.video_label.configure(image='')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Break")
    page = Break1(root, None)
    page.pack(fill="both", expand=True)
    root.mainloop()
