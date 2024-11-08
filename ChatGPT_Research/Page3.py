import tkinter as tk
from tkinter import ttk, messagebox
from Expect import Expect  # Ensure Page4 is correctly implemented
import csv

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure_layout()

    def configure_layout(self):
        self.font_style = ("Helvetica", 12, "bold")
        titleLabel = tk.Label(self, text='Pre-Test Survey', font=("Helvetica", 14, "bold"))
        titleLabel.grid(row=0, column=0, pady=10, padx=10)

        self.questions = [
            {"text": "You would consider yourself new to programming.",
             "choices": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"text": "You would consider yourself familiar with ChatGPT.",
             "choices": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"text": "You enjoy solving complex problems.",
             "choices": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"text": "You would consider yourself in a 'good' mood.",
             "choices": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
            {"text": "You consider yourself good at learning new subjects.",
             "choices": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]}
        ]

        row_offset = 1
        self.answer_vars = {}
        for i, question_data in enumerate(self.questions):
            question_text = question_data["text"]
            choices = question_data["choices"]

            label = tk.Label(self, text=question_text, font=self.font_style)
            label.grid(row=row_offset, column=0, sticky="w", padx=10, pady=2)

            var = tk.StringVar(self, ' ') # Default to empty choice
            self.answer_vars[question_text] = var  # Store the variable with question as key
            for j, choice in enumerate(choices):
                radio_button = tk.Radiobutton(self, text=choice, variable=var, value=choice, font=("Helvetica", 10))
                radio_button.grid(row=row_offset + j + 1, column=0, sticky="w", padx=20, pady=1)

            row_offset += len(choices) + 1

        # Coffee question
        tk.Label(self, text="Have you drank a caffeinated beverage in the past 5 hours?", font=self.font_style).grid(row=row_offset, column=0, sticky="w", padx=10, pady=(10, 20))
        self.caffVar = tk.StringVar(self, 'Select Option')
        self.caffCombo = ttk.Combobox(self, textvariable=self.caffVar, values=['Yes', 'No'], state="readonly")
        self.caffCombo.grid(row=row_offset, column=1, sticky="ew", padx=10)

        row_offset += 1

        # CS course question
        tk.Label(self, text="Which CS course(s) have you taken before?", font=self.font_style).grid(row=row_offset, column=0, sticky="w", padx=10, pady=(10, 20))
        self.csVar = tk.StringVar(self, 'Select Option')
        self.csCombo = ttk.Combobox(self, textvariable=self.csVar, values=['No CS course', 'CS-I', 'CS-II', 'CS-III'], state="readonly")
        self.csCombo.grid(row=row_offset, column=1, sticky="ew", padx=10)

        # Place the submit button below all questions
        self.submitAnswerButton = tk.Button(self, text="Submit", command=self.submitSurveyAnswers, font=("Helvetica", 12))
        self.submitAnswerButton.grid(row=row_offset + 1, column=0, columnspan=2, padx=20, pady=20, sticky="")

    def submitSurveyAnswers(self):
        answers = {question: var.get() for question, var in self.answer_vars.items()}
        caffeine_answer = self.caffVar.get()
        cs_course_answer = self.csVar.get()

        if any(answer == ' ' for answer in answers.values()) or caffeine_answer == 'Select Option' or cs_course_answer == 'Select Option':
            messagebox.showerror("Incomplete", "Please answer all questions before submitting.")
            return

        answers["Have you drank a caffeinated beverage in the past 5 hours?"] = caffeine_answer
        answers["Which CS course(s) have you taken before?"] = cs_course_answer
        self.save_data_to_csv(answers)
        self.controller.show_page(Expect)

    def save_data_to_csv(self, answers):
        filename = self.controller.filename  # Use the filename from the controller
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for question, answer in answers.items():
                writer.writerow([question, answer])  # Write question and answer to the CSV

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pre-Test Survey")
    app = Page3(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
