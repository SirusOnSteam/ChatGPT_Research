import tkinter as tk
from tkinter import messagebox
import webbrowser
import csv
import datetime
import cv2
from pynput.keyboard import Listener
from PIL import Image, ImageTk
from Page8 import Page8

class Page7(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.start_time = None  # This will store the timestamp when the page is shown
        #self.cap = cv2.VideoCapture(0)  # Initialize camera
        self.cap = None
        self.out = None  # Video output initialization

        # Setup the canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Grid the scrollbar and canvas into the frame
        self.scrollbar.grid(row=0, column=1, sticky="nse")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Ensure the canvas expands to fill the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a frame on the canvas to contain all widgets
        self.container_frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0),window=self.container_frame,anchor="nw")

        # Configure the container frame to resize correctly
        self.container_frame.bind("<Configure>",lambda event: self.onFrameConfigure())

        self.video_label = tk.Label(self.container_frame)  # Label to display video frames CAMERA
        self.video_label.grid(row=0, column=2, sticky="ne", padx=10, pady=10) #CAMERA
        self.video_label.grid_remove()


        self.font_style = ("Helvetica", 16, "bold")
        self.title_label = tk.Label(self.container_frame, text="Programming Challenge 2", font=self.font_style)
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Instructions and video button
        self.wLabel = tk.Label(self.container_frame, text='FIRST, Watch this video:', font=self.font_style)
        self.wLabel.grid(row=1, column=0, padx=10, pady=10)
        self.open_link_btn1 = tk.Button(self.container_frame, text="If-Else YouTube Video", command=self.open_youtube1)
        self.open_link_btn1.grid(row=2, column=0, padx=10, pady=10)

        # Labels and buttons for coding challenge
        self.instruction_label = tk.Label(self.container_frame, text="Click this button after watching the entire video:", font=self.font_style)
        self.instruction_label.grid(row=3, column=0, padx=10, pady=5)
        self.instruction_label.grid_remove()  # Initially hidden

        self.timeLimitLabel = tk.Label(self.container_frame, text="You will have 15 minutes to code:", font=self.font_style)
        self.timeLimitLabel.grid(row=4, column=0, padx=10, pady=5)
        self.timeLimitLabel.grid_remove()  # Initially hidden

        self.start_coding_btn = tk.Button(self.container_frame, text="CLICK HERE TO CODE", command=self.display_coding_interface)
        self.start_coding_btn.grid(row=6, column=0, padx=10, pady=10)
        self.start_coding_btn.grid_remove()  # Initially hidden
        # Timer setup
        self.timer_label = tk.Label(self.container_frame, text="15:00", font=self.font_style)
        self.timer_label.grid(row=7, column=0, padx=10, pady=10)
        self.timer_label.grid_remove()  # Initially hidden
        self.key_count = 0

        #Help Image
        self.help_image = Image.open("CH2_Help.PNG")
        self.help_photo = ImageTk.PhotoImage(self.help_image)


    def show_help_image(self): #Help Imahe
        """Display the embedded help image."""
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_label = tk.Label(help_window, image=self.help_photo)
        help_label.pack()   

    def start_keylogger(self):
        """Start the keylogger."""
        self.key_count = 0  # Initialize key count
        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

    def stop_keylogger(self):
        """Stop the keylogger."""
        if hasattr(self, 'listener') and self.listener.is_alive():
            self.listener.stop()

    def on_key_press(self, key):

        if hasattr(key, 'char') and key.char is not None:
            print(f"Key pressed: {key}")
            self.key_count += 1

    def onFrameConfigure(self):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_youtube1(self):
        webbrowser.open_new('https://youtu.be/tvS4hnczG1o')
        #self.open_link_btn1.config(state=tk.DISABLED)
        self.after(746000, self.show_instructions) #746000 ms = 12:26 min

    def show_instructions(self):
        self.instruction_label.grid()
        self.timeLimitLabel.grid()
        self.start_coding_btn.grid()

    def update_video(self):
        """Updates the video frame in the tkinter label."""
        if not self.cap or not self.cap.isOpened():
            print("Camera not initialized or closed.")
            return  # Exit the function if the camera is not initialized or is closed
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
            self.out.write(frame)  # Write frame to video file
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk  # Avoid garbage collection
            self.video_label.config(image=imgtk)
        self.after(10, self.update_video)  # Schedule next frame update

    def initialize_camera(self):
        if not self.cap:  # Check if the camera is not already initialized
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Failed to open the camera.")
                return

        csv_filename = self.controller.get_filename()  #RECORD2
        if csv_filename:
            avi_filename = csv_filename.replace('.csv', '.avi')  # RECORD 2 Replace .csv with .avi

        if not self.out:  # Check if the recorder is not already initialized
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(f"CH2{avi_filename}", self.fourcc, 20.0 ,(320, 240)) 

        self.update_video() 

    def show_and_start_timer(self):
        """Method to start the timer and show the page."""
        self.tkraise()  # Bring this page to the front
        self.video_label.grid()
        if not hasattr(self, 'listener') or not self.listener.is_alive():
            self.start_keylogger()

    def display_coding_interface(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to start coding?"):
            self.start_time = datetime.datetime.now()
            self.initialize_camera()  # Setup the camera when confirmed
            self.show_and_start_timer()
            self.start_timer(900)
            self.show_coding_interface()
            self.start_coding_btn.config(state=tk.DISABLED)
        else: 
            return

    def show_coding_interface(self):
        webbrowser.open_new('https://www.online-python.com/')
        font_style = ("Helvetica", 16, "bold")

        self.timeLimitLabel.grid()

        obj_label = tk.Label(self.container_frame, text="Objective:", font=font_style)
        obj_label.grid(row=8, column=0, sticky="w", padx=10, pady=10)
        ch2 = '''
        Write a program that asks the user to input a temperature (1 pt). 
        Based on the temperature, the program should print different 
        messages:
 
        If the temperature is above 85 degrees Fahrenheit, 
            the program should print: "It's hot! (3 pts)"
        If the temperature is between 70 and 84 degrees Fahrenheit, 
            the program should print: "It's warm. (3 pts)"
        If the temperature is below 70 degrees Fahrenheit, 
            the program should print: "It's cold!" (3 pts)'''

        iLabel = tk.Label(self.container_frame, text= ch2,justify="left", wraplength=500, font=("Helvetica", 12))
        iLabel.grid(row=9, column=0, sticky="w", padx=10, pady=10)

        # Text widget for entering code
        self.text_widget = tk.Text(self.container_frame, height=15, width=50)
        self.text_widget.grid(row=10, column=0, sticky="nsew", padx=10, pady=10)

        submit_btn = tk.Button(self.container_frame, text="Submit", command=self.submit_text)
        submit_btn.grid(row=11, column=0, padx=10, pady=10, sticky="")

        # Create the Help button
        self.help_button = tk.Button(self.container_frame, text="Help", command=self.show_help_image)
        self.help_button.grid(row=11, column=1, padx=10, pady=10)

    def start_timer(self, count):
        """Starts a countdown timer displayed on the label."""
        mins, secs = divmod(count, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        self.timer_label.grid()
        if count > 0:
            self.after(1000, self.start_timer, count - 1)  # Recursive call every second
        else:
            self.timer_label.config(text="Time's up! Submit your code now.", fg="red")

    def submit_text(self):
        user_input = self.text_widget.get("1.0", "end-1c").strip()
        if not user_input:
            messagebox.showerror("Error", "Please do not leave the text area blank.")
            return

        if messagebox.askyesno("Confirm Submission", "Are you sure you want to submit your code?"):
            self.stop_recording()  # Stop the recording when the user submits their code
            completion_time = datetime.datetime.now()
            elapsed_time = (completion_time - self.start_time).total_seconds()
            time_str = f"{elapsed_time // 60} minutes {elapsed_time % 60:.0f} seconds"
            print(f"Submitted text: {user_input}")
            print(f"Time taken for Challenge 2: {time_str}")
            print(f"Challenge 2 completed at: {completion_time.strftime('%Y-%m-%d %H:%M:%S')}")


            # Save the data to a CSV file or any other storage as needed
            self.save_data_to_csv([
            ("Programming Challenge 2", user_input),
            ("PCH 2 Start Time",
                self.start_time.strftime('%Y-%m-%d %H:%M:%S')),
            ("PCH 2 End Time", completion_time.strftime('%Y-%m-%d %H:%M:%S')),
            ("PCH 2 Time Taken", time_str),
            ("PCH 2 Keys Pressed:", self.key_count) 
            ])
            self.stop_keylogger()
            self.controller.show_page(Page8)  # Navigate to the next page 

    def stop_recording(self):
        """Stop recording and release camera resources."""
        if self.out:
            self.out.release()  # Stop saving video data
            self.out = None
        if self.cap.isOpened():
            self.cap.release()  # Release the camera
            self.cap = None

    def save_data_to_csv(self, data_tuples):
        filename = self.controller.filename  # Use the filename managed by the controller
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for title, data in data_tuples:
                writer.writerow([title, data])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Scroll")
    app = Page7(root, None)
    app.pack(fill="both", expand=True)
    app.show_and_start_timer() #CAMERA
    root.mainloop()