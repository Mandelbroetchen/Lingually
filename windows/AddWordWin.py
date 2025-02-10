from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, ttk
import langcodes
import os, json

from windows.Toplevel import *
from windows.CreateProfileWin import *

class AddWordWin(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add a New Word")
        self.geometry("400x300")
        self.resizable(False, False)

        # Word Label and Entry
        tk.Label(self, text="Word:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.word_entry = tk.Entry(self, width=30)
        self.word_entry.grid(row=0, column=1, padx=10, pady=5)

        # Language Label and Dropdown
        tk.Label(self, text="Language:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.languages = sorted([langcodes.get(x).display_name() for x in ["en", "es", "fr", "de", "zh", "ar", "ru", "ja"]])
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, values=self.languages, state="readonly", width=27)
        self.language_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.language_dropdown.current(0)

        # Description Label and Text Field
        tk.Label(self, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        self.description_text = tk.Text(self, width=30, height=5)
        self.description_text.grid(row=2, column=1, padx=10, pady=5)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_word)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def submit_word(self):
        word = self.word_entry.get().strip()
        language = self.language_var.get()
        description = self.description_text.get("1.0", tk.END).strip()

        if not word or not description:
            messagebox.showerror("Error", "Word and Description cannot be empty.")
            return

        word_data = {"word": word, "language": language, "description": description}
        
        # Save to JSON file (or handle data as needed)
        file_path = "words.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(word_data)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        messagebox.showinfo("Success", "Word added successfully!")
        self.destroy()

# Example usage (uncomment below lines if running as a standalone script)
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()  # Hide main window
#     app = AddWordWin(root)
#     app.mainloop()
