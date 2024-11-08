import tkinter as tk
from tkinter import messagebox
import webbrowser
import datetime
import csv
import cv2
from PIL import Image, ImageTk
from Page5 import Page5

class Page4(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        font_style = ("Helvetica", 24, "bold")

        title_label = tk.Label(self, text="Start by Listening to Music...", font=font_style)
        title_label.grid(row=0, column=0, sticky="w")

        i1Label = tk.Label(self, text="1. Watch and listen to this 3 minute video.", font=24)
        i1Label.grid(row=1, column=0, sticky="w")

        self.open_link_btn = tk.Button(self, text="Open YouTube Video", command=self.open_youtube)
        self.open_link_btn.grid(row=2, column=0, pady=20)

        self.i2Label = tk.Label(self, text="2. After Listening to the Music, Start Programming", font=24)
        self.i2Label.grid(row=3, column=0, sticky="w")
        self.i2Label.grid_remove()

        self.go_to_page4_btn = tk.Button(self, text="Start Programming Section", command=self.confirm_start)
        self.go_to_page4_btn.grid(row=4, column=0, pady=20)
        self.go_to_page4_btn.grid_remove()  # Initially hidden; will be shown after YouTube video is opened

        self.video_label = tk.Label(self)  # Label to display video frames
        self.video_label.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

    def setup_camera(self):
        """Set up the camera and start recording."""
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('recording.avi', fourcc, 20.0, (640, 480))
        self.start_time = datetime.datetime.now()
        self.update_video()

    def open_youtube(self):
        """Open YouTube video and start camera recording."""
        webbrowser.open_new('')
        self.setup_camera()
        self.open_link_btn.config(state=tk.DISABLED) 
        self.after(180000, self.show_start_programming) #180000 ms = 3 minutes
        #self.i2Label.grid()
        #self.go_to_page4_btn.grid()  # Show the button to proceed to the next page

    def show_start_programming(self):
        """Show the 'Start Programming' label and button after a delay."""
        self.i2Label.grid()
        self.go_to_page4_btn.grid()

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

    def confirm_start(self):
        """Confirm before starting the programming section and stop recording."""
        if messagebox.askyesno("Confirm", "Are you ready to start the programming section?"):
            self.on_hide()  # Stop recording
            self.go_to_page4()

    def go_to_page4(self):
        """Transition to the next page."""
        self.controller.show_page(Page5)

    def on_hide(self):
        """Release camera and video writer resources."""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.out and self.out.isOpened():
            self.out.release()
            self.out = None
        self.video_label.configure(image='')

    def save_time_to_csv(self, start_time, end_time):
        """Save the start and end times to a CSV file."""
        filename = self.controller.filename
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Page4 Start Time", start_time.strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(["Page4 End Time", end_time.strftime('%Y-%m-%d %H:%M:%S')])

if __name__ == "__main__":
    root = tk.Tk()
    page = Page4(root, None)
    page.pack(fill="both", expand=True)
    root.mainloop()
      
      
