from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser, ttk
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
        self.geometry('480x320')
        self.resizable(False, False)
        
        self.style = ttk.Style()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        for i in [3]:
            self.rowconfigure(i, weight=1)
        for i in [0,1,2,3]:
            self.columnconfigure(i, weight=1)
        padx, pady = 2, 2

        # Enter name
        ttk.Label(self, text="Name:").grid(row=0, column=0, padx=padx, pady=pady, sticky="nsew")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, columnspan=3, padx=padx, pady=pady, sticky="nsew")

        # Select color
        ttk.Label(self, text="Color:").grid(row=1, column=0, padx=padx, pady=pady, sticky="nsew")
        self.color_btn = ttk.Button(self, text="Choose Color", style="Custom.TButton", command=self.choose_color)
        self.color_btn.grid(row=1, column=1, columnspan=3, padx=padx, pady=pady, sticky="nsew")
        self.selected_color = utilities.random_color()
        self.style.configure("Custom.TButton", background=self.selected_color)

        # Function to add languages to the Treeview
        def add_languages():
            selected_languages = utilities.add_language(self.app.config['languages'])
            if selected_languages:
                existing_languages = set(self.languages_tree.get_children())
                for lang in selected_languages:
                    if lang not in existing_languages:
                        self.languages_tree.insert("", "end", iid=lang, values=(lang,))
    
        # Function to remove selected languages from the Treeview
        def remove_languages():
            selected_items = self.languages_tree.selection()
            for item in selected_items:
                self.languages_tree.delete(item)

        # Button to add languages
        self.add_button = ttk.Button(self, text="Add Desired Languages", command=add_languages)
        self.add_button.grid(row=2, column=0, padx=padx, pady=pady, sticky="nsew")

        # Button to remove selected languages
        self.remove_button = ttk.Button(self, text="Remove Selected", command=remove_languages)
        self.remove_button.grid(row=2, column=1, padx=padx, pady=pady, sticky="nsew")

        # Treeview to display selected languages
        self.languages_tree = utilities.ToggleTreeview(self, columns=("Language"), show="headings", height=5)
        self.languages_tree.heading("Language", text="Desired Languages")
        self.languages_tree.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady, sticky="nsew")

        # Function to add natives to the Treeview
        def add_natives():
            selected_natives = utilities.add_language(self.app.config['languages'])
            if selected_natives:
                existing_natives = set(self.natives_tree.get_children())
                for lang in selected_natives:
                    if lang not in existing_natives:
                        self.natives_tree.insert("", "end", iid=lang, values=(lang,))

        # Function to remove selected natives from the Treeview
        def remove_natives():
            selected_items = self.natives_tree.selection()
            for item in selected_items:
                self.natives_tree.delete(item)

        # Button to add natives
        self.add_button = ttk.Button(self, text="Add Native Languages", command=add_natives)
        self.add_button.grid(row=2, column=2, padx=padx, pady=pady, sticky="nsew")

        # Button to remove selected natives
        self.remove_button = ttk.Button(self, text="Remove Selected", command=remove_natives)
        self.remove_button.grid(row=2, column=3, padx=padx, pady=pady, sticky="nsew")

        # Treeview to display selected natives
        self.natives_tree = utilities.ToggleTreeview(self, columns=("NativeLanguage",), show="headings", height=5)
        self.natives_tree.heading("NativeLanguage", text="Native Languages")

        self.natives_tree.grid(row=3, column=2, columnspan=2, padx=padx, pady=pady, sticky="nsew")

        # Submit
        def on_click():
            name = self.name_entry.get()
            color = self.selected_color if self.selected_color else "None"
            languages = [self.languages_tree.item(item, "values")[0] for item in self.languages_tree.get_children()]
            natives = [self.natives_tree.item(item, "values")[0] for item in self.natives_tree.get_children()]
            self.create_profile(name, color, languages, natives)

        submit_btn = ttk.Button(self, text="Create Profile", command=on_click)
        submit_btn.grid(row=4, column=0, columnspan=4, padx=padx, pady=pady, sticky="nsew")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose a color")[1]  # Get HEX color
        if color_code:
            self.selected_color = color_code
            self.style.configure("Custom.TButton", background=color_code)
    
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
                    ...
            self.destroy()
        else:
            messagebox.showerror("Error", f'Profile {name} already exists.')
            self.name_entry.insert(0, "")
