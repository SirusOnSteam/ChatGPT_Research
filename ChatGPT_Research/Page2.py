import tkinter as tk
from tkinter import ttk, messagebox
from Page3 import Page3
import csv
import re


class Page2(tk.Frame):

  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller

    self.setup_ui()

  def setup_ui(self):
    font_style = ("Helvetica", 12, "bold")
    titleLabel = tk.Label(self,
                          text='Demographics Questionnaire',
                          font=("Helvetica", 14, "bold"))
    titleLabel.grid(row=0, column=0, columnspan=2, pady=(20, 30))

    # Configuration for entries and dropdowns
    self.setup_entries(font_style)
    self.setup_comboboxes(font_style)

    submitButton = tk.Button(self,text="Submit",command=self.submit_form,font=font_style)
    submitButton.grid(row=9,column=0,columnspan=2,pady=(30, 10),sticky="ew")

  def setup_entries(self, font_style):
    self.ageEntry = tk.Entry(self)
    self.ageEntry.grid(row=1, column=1, sticky="ew", padx=10)
    tk.Label(self, text="What is your age?",font=font_style).grid(row=1,column=0,sticky="w",padx=10,pady=(10, 20))

    self.majorEntry = tk.Entry(self)
    self.majorEntry.grid(row=2, column=1, sticky="ew", padx=10)
    tk.Label(self, text="What is your major?",font=font_style).grid(row=2,column=0,sticky="w",padx=10,pady=(10, 20))

  def setup_comboboxes(self, font_style):
    self.yearCombo = ttk.Combobox(
        self,
        values=['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate','UHD Staff','Other'],
        state="readonly")
    self.yearCombo.set('Select Year')
    self.yearCombo.grid(row=3, column=1, sticky="ew", padx=10)
    tk.Label(self, text="What is your UHD status?",font=font_style).grid(row=3,column=0,sticky="w",padx=10,pady=(10, 20))

    self.raceCombo = ttk.Combobox(self,values=['Asian', 'Black/African American','Hispanic/Latino', 'White', 'Other'],state="readonly")
    self.raceCombo.set('Select Race')
    self.raceCombo.grid(row=4, column=1, sticky="ew", padx=10)
    tk.Label(self, text="What is your race/ethnicity?",font=font_style).grid(row=4,column=0,sticky="w",padx=10,pady=(10, 20))

    self.genderCombo = ttk.Combobox(self,values=['Male', 'Female', 'Other'],state="readonly")
    self.genderCombo.set('Select Gender')
    self.genderCombo.grid(row=5, column=1, sticky="ew", padx=10)
    tk.Label(self, text="What is your gender?",font=font_style).grid(row=5,column=0,sticky="w",padx=10,pady=(10, 20))

    #Taken out and moved to 'Pre-test survey'.

    #self.caffCombo = ttk.Combobox(self,values=['Yes', 'No'],state="readonly")
    #self.caffCombo.set('Select Option')
    #self.caffCombo.grid(row=6, column=1, sticky="ew", padx=10)
    #tk.Label(self, text="Have you drank a caffeinated beverage in the past 5 hours?",font=font_style).grid(row=6,column=0,sticky="w",padx=10,pady=(10, 20))

  def is_valid_age(self, age):
    try:
      age = int(age)
      return 0 <= age <= 100
    except ValueError:
      return False

  def is_valid_major(self, major):
    # This regular expression checks if the major consists only of letters and spaces
    return re.fullmatch(r'[A-Za-z\s]+', major) is not None

  def submit_form(self):
    age = self.ageEntry.get().strip()
    major = self.majorEntry.get().strip()
    year = self.yearCombo.get()
    ethnicity = self.raceCombo.get()
    gender = self.genderCombo.get()
    #caffeine = self.caffCombo.get() --Taken out and moved to pre-test survey.

    if not self.is_valid_age(age):
      messagebox.showerror("Error", "Age must be a number between 0 and 100.")
      return

    if not self.is_valid_major(major):
      messagebox.showerror("Error",
                           "Major must only contain letters and spaces.")
      return

    if ethnicity == "Select Race":
      messagebox.showerror("Error", "Please select your race/ethnicity.")
      return
    if gender == "Select Gender":
      messagebox.showerror("Error", "Please select your gender.")
      return
    if year == "Select Year":
      messagebox.showerror("Error", "Please select your academic year.")
      return
    
    #Moved to 'Pre-test'
    #if caffeine == "Select Option":
      #messagebox.showerror("Error", "Please select an answer for caffeine.")
      #return

    # If all validations pass, proceed with data saving and changing the page
    self.save_data_to_csv([("Age", age), ("Major", major), ("Year", year),
                           ("Race/Ethnicity", self.raceCombo.get()),
                           ("Gender", self.genderCombo.get()),
                           #("Caffeinated Drink?", self.caffCombo.get())
                           ])
    self.controller.show_page(Page3)

  def save_data_to_csv(self, data_tuples):
    filename = self.controller.filename  # Retrieve the filename from the controller
    with open(filename, 'a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      for title, data in data_tuples:
        writer.writerow([
            title, data
        ])  # Write each data point in a new row under the correct header
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Demographics Section")
    app = Page2(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()






