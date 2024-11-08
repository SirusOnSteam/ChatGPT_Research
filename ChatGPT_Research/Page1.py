import tkinter as tk
from tkinter import messagebox
from Page2 import Page2
import re 
import csv

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        font_style = ("Helvetica", 24, "bold")
        tk.Label(self, text="Behavioral Analysis Test", font=font_style).grid(row=0, column=1)

        description = """
        Welcome! Thank you for participating in our Local Research Experience
        project. Today we will be testing for the following items:

            - Body Motion
            - Facial Motion
            - Heart Rate
            - Mouse Placement
                  
        You will be asked to complete a demographic questionnaire, pre-survey,
        and a post-survey at the end of testing.

        Thank you for your time and cooperation! We greatly appreciate it!\n"""

        tk.Label(self, text=description).grid(row=1, column=0, columnspan=3)

        tk.Label(self, text="Enter Name: ").grid(row=2, column=0)
        self.fnameEntry = tk.Entry(self)
        self.fnameEntry.grid(row=2, column=1)

        tk.Label(self, text="Enter Last Name: ").grid(row=3, column=0)
        self.lnameEntry = tk.Entry(self)
        self.lnameEntry.grid(row=3, column=1)

        tk.Label(self, text="Enter E-Mail: ").grid(row=4, column=0)
        self.emEntry = tk.Entry(self)
        self.emEntry.grid(row=4, column=1)

        submitButton = tk.Button(self, text="Submit", command=self.submit)
        submitButton.grid(row=5, column=1)

    def is_valid_email(self, email):
        """Validate the email address using a regular expression."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email):
            return True
        return False

    def submit(self):
        fname = self.fnameEntry.get().strip()
        lname = self.lnameEntry.get().strip()
        email = self.emEntry.get().strip()
        if fname and lname and email:
            if not self.is_valid_email(email):
                messagebox.showerror("Invalid Email", "Please enter a valid email address.")
                return
            # Generate a filename based on the user's name to keep it unique
            filename = f"{fname}_{lname}.csv"
            self.controller.filename = filename # Store filename in the controller
            self.save_data_to_csv([
                ("First Name", fname),
                ("Last Name", lname),
                ("Email", email)
            ], filename)
            self.controller.show_page(Page2)
        else:
            messagebox.showerror("Error", "Please do not leave any areas blank.")

    def save_data_to_csv(self, data_tuples, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Field", "Data"])  # Write header
            for title, data in data_tuples:
                writer.writerow([title, data])  # Write each field in new row

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Introductionary Section")
    app = Page1(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()




