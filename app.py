from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser
import langcodes
from mistralai import Mistral


import os, sys
import re, json

import utilities



class App:
    def __init__(self, config, llm):
        self.llm = llm
        self.config = config
        self.root = tk.Tk()
        self.root.app = self

        self.root.title(self.name)
        self.root.geometry('300x200')

        if len(self.profiles_names) == 0:
            create_profile_win = CreateProfileWin(self.root)
            create_profile_win.focus_set()

    @property
    def name(self):
        return self.config['name']

    @property
    def profiles_names(self):
        profiles_path = Path(self.config['paths']['profiles'])
        profiles_names = [dir.name for dir in profiles_path.iterdir() if dir.is_dir()]
        return profiles_names

class Toplevel(tk.Toplevel):
    @property
    def app(self):
        try:
            return self.master.app
        except AttributeError:
            return self.master
    
class CreateProfileWin(Toplevel):
    def __init__(self, parent, title="Create Profile"):
        super().__init__(parent)
        self._title = title
        self.title(self._title)
        self.geometry('300x250')

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Enter name
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Select color
        tk.Label(self, text="Color:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.color_btn = tk.Button(self, text="Choose Color", command=self.choose_color)
        self.color_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.selected_color = None

        # Function to add languages to the Listbox
        def add_languages():
            selected_languages = utilities.add_language(self.app.config['languages'])
            if selected_languages:
                existing_languages = self.languages_listbox.get(0, tk.END)
                for lang in selected_languages:
                    if lang not in existing_languages:  # Avoid duplicates
                        self.languages_listbox.insert(tk.END, lang)

        # Function to remove selected languages from the Listbox
        def remove_languages():
            selected_indices = self.languages_listbox.curselection()
            for index in reversed(selected_indices):  # Reverse to avoid shifting issues
                self.languages_listbox.delete(index)

        # Button to add languages
        self.add_button = tk.Button(self, text="Add Languages", command=add_languages)
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Button to remove selected languages
        self.remove_button = tk.Button(self, text="Remove Selected", command=remove_languages)
        self.remove_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Listbox to display selected languages
        self.languages_listbox = tk.Listbox(self, height=5, width=30, selectmode=tk.MULTIPLE)
        self.languages_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

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
        self.add_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Button to remove selected natives
        self.remove_button = tk.Button(self, text="Remove Selected", command=remove_natives)
        self.remove_button.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Listbox to display selected natives
        self.natives_listbox = tk.Listbox(self, height=5, width=30, selectmode=tk.MULTIPLE)
        self.natives_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Submit
        submit_btn = tk.Button(self, text="Create Profile", command=self.create_profile)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose a color")[1]  # Get HEX color
        if color_code:
            self.selected_color = color_code
            self.color_btn.config(bg=color_code)
    
    def create_profile(self):
        name = self.name_entry.get()
        color = self.selected_color if self.selected_color else "None"
        languages = self.languages_listbox.get(0, tk.END)
        natives = self.natives_listbox.get(0, tk.END)

        new_dir_path = Path(self.app.config["paths"]["profiles"]) / name

        if not new_dir_path.exists():
            new_dir_path.mkdir(parents=True)
            with open(new_dir_path / "info.json", "w") as f:
                json.dump({
                    "name": name,
                    "color": color,
                    "languages": languages,
                    "natives": natives
                }, f)
            messagebox.showinfo("Success", f'Created Profile "{name}".')
            self.destroy()
        else:
            messagebox.showerror("Error", f'Profile "{name}" already exists.')
            self.__init__(self.master)



if __name__ == "__main__":
    # Load LLM client
    load_dotenv()
    api_key = os.getenv("API_KEY")
    llm = Mistral(api_key)

    # Load configuration file
    with open('config.json','r') as f:
        config = json.load(f)

    # Creat Directories if don't exist
    for key, path in config['paths'].items():
        os.makedirs(path, exist_ok=True)
    
    # Start the App
    app = App(config, llm)
    app.root.mainloop()


'''chat_response = client.chat.complete(
    model=model,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ],
    temperature=0
).choices[0].message.content'''