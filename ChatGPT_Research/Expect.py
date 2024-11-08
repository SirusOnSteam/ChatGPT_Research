import tkinter as tk
from tkinter import messagebox
import webbrowser
from Page4 import Page4


class Expect(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        titleLabel = tk.Label(self,
                              text="Watch this Video on What to Expect:",
                              font=("Helvetica", 20, "bold"))
        titleLabel.grid(row=0, column=0, pady=10, padx=10, sticky='w')

        # Button to open YouTube video
        self.open_link_btn = tk.Button(self,
                                       text="Watch Introduction Video",
                                       command=self.open_youtube)
        self.open_link_btn.grid(row=1, column=0, pady=10, padx=10)

        self.nextPageLabel = tk.Label(
            self,
            text="Go to the Next Page after watching the Video:",
            font=("Helvetica", 20))
        self.nextPageLabel.grid(row=2, column=0)
        self.nextPageLabel.grid_remove()

        # Button to navigate to the next page, initially hidden
        self.next_page_button = tk.Button(self,
                                          text="Go to Next Page",
                                          command=self.go_to_next_page)
        self.next_page_button.grid(row=3, column=0)
        self.next_page_button.grid_remove()  # Hide this button initially

    def open_youtube(self):
        """Open a YouTube link in the web browser."""
        webbrowser.open_new('https://youtu.be/tYoheva8-Sg')
        self.after(300000, self.show_next_page_button)  #5 min = 300000 ms

    def show_next_page_button(self):
        self.nextPageLabel.grid()
        self.next_page_button.grid(
        )  # Show the "Next Page" button after the video link is opened

    def go_to_next_page(self):
        """Navigate to the next page."""
        self.controller.show_page(Page4)

    def on_hide(self):
        """Handle cleanup when the frame is hidden or the application is closed."""
        print("Clean up resources if necessary.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Expect(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
