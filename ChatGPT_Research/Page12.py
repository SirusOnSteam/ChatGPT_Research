import tkinter as tk
from tkinter import ttk, messagebox

class Page12(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        font_style = ("Helvetica", 12, "bold")  # Reduced font size for better fit
        titleLabel = tk.Label(self, text = 'Thank You for Participating!', font=font_style)
        titleLabel.grid(row=0, column=0)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Survey Example")
    page = Page12(root, None)
    page.pack(fill="both", expand=True)
    root.mainloop()