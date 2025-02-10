from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser
import langcodes
from mistralai import Mistral

import os, sys
import re, json

import utilities
from windows.Toplevel import *

class CreateProfileWin(Toplevel):
    def __init__(self, parent, title="Create Profile"):
        super().__init__(parent)
        self._title = title
        self.title(self._title)
        self.geometry('300x600')

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Enter name
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Select color
        tk.Label(self, text="Color:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.color_btn = tk.Button(self, text="Choose Color", command=self.choose_color)
        self.color_btn.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.selected_color = None

        # Function to add languages to the Listbox
        def add_languages():
            selected_languages = utilities.add_language(self.app.config['languages'])
            if selected_languages:
                existing_languages = self.languages_listbox.get(0, tk.END)
                for lang in selected_languages:
                    if lang not in existing_languages:
                        self.languages_listbox.insert(tk.END, lang)

        # Function to remove selected languages from the Listbox
        def remove_languages():
            selected_indices = self.languages_listbox.curselection()
            for index in reversed(selected_indices):  # Reverse to avoid shifting issues
                self.languages_listbox.delete(index)

        # Button to add languages
        self.add_button = tk.Button(self, text="Add Languages", command=add_languages)
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Button to remove selected languages
        self.remove_button = tk.Button(self, text="Remove Selected", command=remove_languages)
        self.remove_button.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        # Listbox to display selected languages
        self.languages_listbox = tk.Listbox(self, height=5, width=30, selectmode=tk.MULTIPLE)
        self.languages_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Function to add natives to the Listbox
        def add_natives():
            selected_natives = utilities.add_language(self.app.config['languages'])
            if selected_natives:
                existing_natives = self.natives_listbox.get(0, tk.END)
                for lang in selected_natives:
                    if lang not in existing_natives:  # Avoid duplicates
                        self.natives_listbox.insert(tk.END, lang)

        # Function to remove selected natives from the Listbox
        def remove_natives():
            selected_indices = self.natives_listbox.curselection()
            for index in reversed(selected_indices):  # Reverse to avoid shifting issues
                self.natives_listbox.delete(index)

        # Button to add natives
        self.add_button = tk.Button(self, text="Add natives", command=add_natives)
        self.add_button.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        # Button to remove selected natives
        self.remove_button = tk.Button(self, text="Remove Selected", command=remove_natives)
        self.remove_button.grid(row=4, column=1, padx=10, pady=5, sticky="nsew")

        # Listbox to display selected natives
        self.natives_listbox = tk.Listbox(self, height=5, width=30, selectmode=tk.MULTIPLE)
        self.natives_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Submit
        def on_click():
            name = self.name_entry.get()
            color = self.selected_color if self.selected_color else "None"
            languages = self.languages_listbox.get(0, tk.END)
            natives = self.natives_listbox.get(0, tk.END)
            self.create_profile(name, color, languages, natives)
        submit_btn = tk.Button(self, text="Create Profile", command=on_click)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose a color")[1]  # Get HEX color
        if color_code:
            self.selected_color = color_code
            self.color_btn.config(bg=color_code)
    
    def create_profile(self, name, color, languages, natives):
        if name == "" or name is None:
            messagebox.showerror("Error", f'You need to enter a name to create a profile. ')
            return

        new_dir_path = Path(self.app.config["paths"]["profiles"]) / name

        if not new_dir_path.exists():
            new_dir_path.mkdir(parents=True)
            with open(new_dir_path / "info.json", "w") as f:
                json.dump({
                    "name": name,
                    "color": color,
                    "languages": languages,
                    "natives": natives
                }, f, indent=4)
            with open(new_dir_path / "vocabs.json", "w") as f:
                json.dump(dict(zip(languages, [{} for l in languages])), f, indent=4)
            if messagebox.askyesno("Success", f"Do you want to switch profile to {name}"):
                self.profile = name
                if messagebox.askyesno("", "Do you want to be evaluated?"):
                    # Call the eveluation window
                    ...
            self.destroy()
        else:
            messagebox.showerror("Error", f'Profile {name} already exists.')
            self.name_entry.insert(0, "")