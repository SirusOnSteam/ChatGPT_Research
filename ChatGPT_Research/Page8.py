import tkinter as tk
from tkinter import ttk, messagebox
import csv
from Break2 import Break2  # Ensure Page7 is properly implemented

class Page8(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.font_style = ("Helvetica", 12)
        self.setup_ui()

    def setup_ui(self):
        titleLabel = tk.Label(self, text='NASA TLX Survey for Challenge 2: ', font=("Helvetica", 14, "bold"))
        titleLabel.grid(row=0, column=0, columnspan=5, pady=20, padx=10, sticky='w')

        instructionLabel = tk.Label(self, text='Slide the blue index to indicate your response:', font=("Helvetica", 14, "bold"))
        instructionLabel.grid(row=1, column=0, columnspan=5, pady=20, padx=10, sticky='w')

        self.questions = [
            "Mental Demand: How mentally demanding was the task?",
            "Physical Demand: How physically demanding was the task?",
            "Temporal Demand: How hurried or rushed was the pace of the task?",
            "Performance: How successful were you in accomplishing what you were asked to do?",
            "Effort: How hard did you have to work to accomplish your level of performance?",
            "Frustration: How insecure, discouraged, irritated, stressed, and annoyed were you?"
        ]

        self.sliders = []
        self.value_labels = []
        row_offset = 2
        for i, question in enumerate(self.questions):
            label = tk.Label(self, text=question, font=self.font_style, wraplength=400)
            label.grid(row=row_offset, column=0, sticky="w", padx=10, pady=10, columnspan=4)

            low_label = tk.Label(self, text="Very Low", font=("Helvetica", 10))
            low_label.grid(row=row_offset+1, column=0, padx=10, pady=5, sticky="w")

            value_label = tk.Label(self, text="0   %", font=("Helvetica", 10))
            value_label.grid(row=row_offset+1, column=2, padx=10, pady=5)
            self.value_labels.append(value_label)

            slider = ttk.Scale(self, from_=0, to=100, orient="horizontal", length=300, command=lambda value, idx=i: self.update_slider_label(idx, value))
            slider.grid(row=row_offset+1, column=1, padx=10, pady=5)
            self.sliders.append(slider)
            
            high_label = tk.Label(self, text="Very High", font=("Helvetica", 10))
            high_label.grid(row=row_offset+1, column=3, padx=10, pady=5, sticky="e")
            
            row_offset += 2

        submit_button = tk.Button(self, text="Submit", command=self.submit_survey_answers, font=("Helvetica", 12))
        submit_button.grid(row=row_offset, column=0, columnspan=4, padx=20, pady=30, sticky="")

    def update_slider_label(self, index, value):
        # Update the label next to slider with the current value
        self.value_labels[index].config(text="{:.0f}   %".format(float(value)))

    def submit_survey_answers(self):
        if messagebox.askyesno("Confirm Submission", "Are you sure you want to submit your responses?"):
            scores = [slider.get() for slider in self.sliders]
            results = dict(zip(self.questions, scores))
            print("Survey Results:", results)
            self.save_data_to_csv(results)  # Save results to CSV
            self.controller.show_page(Break2)
        else:
            return

    def save_data_to_csv(self, data_dict):
        filename = self.controller.filename  # Use filename from controller
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for question, answer in data_dict.items():
                writer.writerow(["PCH 2 " + question, "{:.2f}".format(answer)])  # Write question and answer in two columns

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Survey Example")
    page = Page8(root, None)
    page.pack(fill="both", expand=True)
    root.mainloop()
