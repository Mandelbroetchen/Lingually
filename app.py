from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser
import langcodes
import webbrowser
from mistralai import Mistral

import os, sys
import re, json

import utilities
from windows.CreateProfileWin import *
from windows.AddWordWin import *

class App:
    def __init__(self, config, llm):
        self.llm = llm
        self.config = config
        self.root = tk.Tk()
        self.root.app = self
        self.user = None

        self.root.title(self.name)
        self.root.geometry('640x480')

        menu_bar = tk.Menu(self.root)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add word", command=lambda: AddWordWin(self.root))
        edit_menu.add_command(label="Add words from text")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Profile Menu
        profile_menu = tk.Menu(menu_bar, tearoff=0)
        profile_menu.add_command(label="New profile", command=lambda: CreateProfileWin(self.root))
        menu_bar.add_cascade(label="Profile", menu=profile_menu)

        # Display Menu
        display_menu = tk.Menu(menu_bar, tearoff=0)
        for res in self.config["resolutions"]:
            display_menu.add_command(label=res, command=lambda res=res: self.root.geometry(res))
        menu_bar.add_cascade(label="Display", menu=display_menu)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: webbrowser.open(self.config["about"]))
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)


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
    
    def llm_single_reply(self, user_message):
        chat_response = self.llm_client.chat.complete(
            model=self.llm,
            messages=[
                {"role": "system", "content": "Answer concisely, as few words as possible. "},
                {"role": "user", "content": user_message},
            ],
            temperature=0
        ).choices[0].message.content


    




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