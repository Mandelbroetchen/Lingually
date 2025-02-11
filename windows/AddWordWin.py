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

        padx, pady = 2, 2
        
        for i in [2]:
            self.rowconfigure(i, weight=1)
        for i in [1]:
            self.columnconfigure(i, weight=1)

        # Word Label and Entry
        tk.Label(self, text="Word:").grid(row=0, column=0, padx=padx, pady=pady, sticky="w")
        self.word_entry = tk.Entry(self, width=30)
        self.word_entry.grid(row=0, column=1, padx=padx, pady=pady, sticky="nsew")

        # Language Label and Dropdown
        tk.Label(self, text="Language:").grid(row=1, column=0, padx=padx, pady=pady, sticky="w")
        self.languages = sorted(self.app.profile_info["languages"])
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, values=self.languages, state="readonly", width=27)
        self.language_dropdown.grid(row=1, column=1, padx=padx, pady=pady, sticky="nsew")
        try: self.language_dropdown.current(0)
        except: pass

        # Description Label and Text Field
        tk.Label(self, text="Definition:").grid(row=2, column=0, padx=padx, pady=pady, sticky="nw")
        self.description_text = tk.Text(self, width=30, height=5)
        self.description_text.grid(row=2, column=1, columnspan=1, padx=padx, pady=pady, sticky="nsew")
        
        # Submit Button
        self.generate_button = tk.Button(self, text="Generate Definition", command=self.generate)
        self.generate_button.grid(row=3, column=1, columnspan=1, padx=padx, pady=pady, sticky="nsew")
        
        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_word)
        self.submit_button.grid(row=4, column=1, columnspan=1, padx=padx, pady=pady, sticky="nsew")
    
    def generate(self):
        word = self.word_entry.get().strip()
        definition = self.app.llm_word_definition(f'Give the definition of "{word}"')
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", definition)
    
    def submit_word(self):
        word = self.word_entry.get().strip()
        language = self.language_var.get()
        description = self.description_text.get("1.0", tk.END).strip()

        if not word or not description:
            messagebox.showerror("Error", "Word and Description cannot be empty.")
            return
        if self.app.profile_info is None:
            return
                
        self.app.profile_write_vocabs({
            language: {
                word: description
            }
        })

        self.destroy()
