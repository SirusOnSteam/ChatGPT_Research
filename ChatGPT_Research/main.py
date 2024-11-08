import tkinter as tk
from datetime import datetime
import csv
#import cv2
#from tkinter import ttk, messagebox

from Page1 import Page1
from Page2 import Page2
from Page3 import Page3
from Expect import Expect
from Page4 import Page4
from Page5 import Page5
from Page6 import Page6
from Break1 import Break1
from Page7 import Page7
from Page8 import Page8
from Break2 import Break2
from Page9 import Page9
from Page10 import Page10
from Page11 import Page11
from Page12 import Page12

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        #self.participant_name = None  # Initially no name

        self.title("Behavioral Analysis Test")

        # Calculate the appropriate size and position for the window
        screen_width = self.winfo_screenwidth()  # Get the width of the screen
        screen_height = self.winfo_screenheight()  # Get the height of the screen
        window_width = screen_width // 2  # Use half of the screen width
        window_height = screen_height  # Use the full height of the screen

        # Set the geometry of the main window to occupy the left half of the screen
        self.geometry(f"{window_width}x{window_height}+0+0")  # +0+0 positions it at the top left

        # Create a container frame that will contain all the pages
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionary to hold all the pages
        self.pages = {}

        # Loop over the pages and initialize them within the container
        for PageClass in (Page1, Page2, Page3, Page4, Expect, Page5, Page6,Break1, Page7, Page8,Break2, Page9,
                          Page10, Page11, Page12):
            page = PageClass(parent=self.container, controller=self)
            self.pages[PageClass] = page
            page.grid(row=0, column=0, sticky="nsew")

        # Display the initial page
        self.show_page(Page1)

    def set_filename(self, first_name, last_name):
        """Create a new filename based on the user's name if it hasn't been created yet."""
        if not self.filename:
            self.filename = f"{first_name}_{last_name}.csv"
            self.create_csv()  # Initialize the file with headers

    def create_csv(self):
        """Create a CSV file and write the header."""
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Data"])

    def get_filename(self):
        """Retrieve the current filename to use."""
        return self.filename

    def show_page(self, page_class):
        """Bring a given page to the front to be visible."""
        page = self.pages[page_class]        
        if page_class == Page5:
            page.show_and_start_timer()
        elif page_class == Page7:
            page.show_and_start_timer()
        elif page_class == Page9:
            page.show_and_start_timer()
        elif page_class == Break1:
            page.on_show_frame()
        elif page_class == Break2:
            page.on_show_frame()
        else:
            page.tkraise()  # This method brings the page to the top of the stacking order

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()