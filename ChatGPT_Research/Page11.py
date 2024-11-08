import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Frame
import csv
from Page12 import Page12

class Page11(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.font_style = ("Helvetica", 12, "bold")
        self.answer_vars = {}
        self.configure_layout()

    def configure_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        titleLabel = tk.Label(self.scrollable_frame, text='Post-Test Survey', font=self.font_style)
        titleLabel.grid(row=0, column=0)

        self.questions = [
            "You believe you learned something from this session.",
            "You had a difficult time learning the programming material.",
            "You felt stressed attempting to solve the challenges.",
            "You are interested in programming and want to continue learning.",
            "Please share your feedback on the teaching methods used and your overall experience."
        ]
        choices = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

        row_offset = 1
        for question in self.questions[:-1]:
            label = tk.Label(self.scrollable_frame, text=question, font=self.font_style)
            label.grid(row=row_offset, column=0, sticky="w", padx=10, pady=2)

            var = tk.StringVar(self, ' ')  # Default to first choice
            self.answer_vars[question] = var
            for j, choice in enumerate(choices):
                radio_button = tk.Radiobutton(self.scrollable_frame, text=choice, variable=var, value=choice, font=("Helvetica", 10))
                radio_button.grid(row=row_offset + j + 1, column=0, sticky="w", padx=20, pady=1)

            row_offset += len(choices) + 1

        last_question = self.questions[-1]
        feedback_label = tk.Label(self.scrollable_frame, text=last_question, font=self.font_style)
        feedback_label.grid(row=row_offset, column=0, sticky="w", padx=10, pady=2)
        
        self.feedback_text = tk.Text(self.scrollable_frame, height=4, width=50)  # Multi-line text widget
        self.feedback_text.grid(row=row_offset + 1, column=0, sticky="w", padx=20, pady=1)
        row_offset += 2

        self.submitAnswerButton = tk.Button(self.scrollable_frame, text="Submit", command=self.confirmSubmit, font=("Helvetica", 12))
        self.submitAnswerButton.grid(row=row_offset, column=0, padx=20, pady=20, sticky="")

        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def confirmSubmit(self):
        if messagebox.askyesno("Confirm Submission", "Are you ready to submit your answers?"):
            self.submitSurveyAnswers()
        else:
            return

    def submitSurveyAnswers(self):
        answers = {question: var.get() for question, var in self.answer_vars.items()}
        last_answer = self.feedback_text.get("1.0", "end-1c").strip()
        if last_answer:
            answers[self.questions[-1]] = last_answer
        else:
            answers[self.questions[-1]] = "No feedback provided"
        if any(answer == ' ' for answer in answers.values()):
            messagebox.showerror("Incomplete", "Please answer all questions before submitting.")
            return
        print("Survey Answers:", answers)
        self.save_data_to_csv(answers)
        self.controller.show_page(Page12)

    def save_data_to_csv(self, answers):
        filename = self.controller.filename
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for question, answer in answers.items():
                writer.writerow([question, answer])

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = Page11(root, None)
    app.pack(fill="both", expand=True)
    root.mainloop()
