from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser
import langcodes
import webbrowser
from mistralai import Mistral
from PIL import Image, ImageTk


import os, sys
import re, json

import utilities
from windows.CreateProfileWin import *
from windows.AddWordWin import *
from windows.SwitchProfileWin import *
from windows.SetModelWin import*
class App:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.root.app = self
        self.profile = None

        self.root.title(self.name)
        self.root.geometry('640x480')
        icon_image = Image.open("icon.png")
        self.icon = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(True, self.icon)

        menu_bar = tk.Menu(self.root)
        # Profile Menu
        profile_menu = tk.Menu(menu_bar, tearoff=0)
        profile_menu.add_command(label="New Profile", command=lambda: CreateProfileWin(self.root))
        profile_menu.add_command(label="Switch Profile", command=lambda: SwitchProfileWin(self.root))
        profile_menu.add_command(label="Manage Profiles*")

        menu_bar.add_cascade(label="Profile", menu=profile_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add Word", command=lambda: AddWordWin(self.root))
        edit_menu.add_command(label="Add Words from Paragraph*")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Settings Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Model Setting*", command=lambda: SetModelWin(self.root))
        edit_menu.add_command(label="APP Preference*")
        edit_menu.add_command(label="Profile Preference*")
        menu_bar.add_cascade(label="Settings", menu=edit_menu)
        
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

        self.root.after(10,self.after)
    
    def after(self):
        if len(self.profile_names) == 0:
            create_profile_win = CreateProfileWin(self.root)
            create_profile_win.focus_set()
        
        if ((not self.config["login_with"] in ("main_profile", "last_profile")
        ) or (
            self.config["login_with"] == "main_profile" and self.config["main_profile"] is None
        ) or (
            self.config["login_with"] == "last_profile" and self.config["last_profile"] is None
        )) and len(self.profile_names) > 0:
            win = SwitchProfileWin(self.root)

    @property
    def name(self):
        return self.config['name']

    @property
    def profile_names(self):
        profiles_path = Path(self.config['paths']['profiles'])
        profile_names = [dir.name for dir in profiles_path.iterdir() if dir.is_dir()]
        return profile_names
    
    def get_profile_info(self, profile_name):
        path = Path(self.config["paths"]["profiles"])/profile_name/"info.json"
        if path.exists():
            with open(str(path),'r') as f:
                info = json.load(f)
            return info
        else:
            return None
    
    @property
    def profile_info(self):
        return self.get_profile_info(self.profile)
    
    def profile_write_vocabs(self, new_vocabs):
        path = Path(self.config["paths"]["profiles"])/self.profile/"vocabs.json"
        with open(path, 'r') as f:
            vocabs = json.load(f)
            for lan, new_words in new_vocabs.items():
                if lan in vocabs:
                    vocabs[lan].update(new_words)
                else:
                    vocabs[lan] = new_words
        
        with open(path, 'w') as f:
            json.dump(vocabs, f, indent=4)

    def llm_reply(self, user_message, *system_messages):
        if self.config["model"]["api_key"] is None:
            # Open set model window
            ...
            return
        llm_client = Mistral(config["model"]["api_key"])
        messeges = [
            {"role": "system", "content": msg} for msg in system_messages
        ] + [{"role": "user", "content": user_message}]
        print(messeges)
        chat_response = llm_client.chat.complete(
            model=self.config["model"]["name"],
            messages=messeges,
            temperature=0
        ).choices[0].message.content
        return chat_response

    def llm_simple_reply(self, user_message):
        return self.llm_reply(user_message, self.config["system_prompts"]["simple_reply"])
    
    def llm_word_definition(self, user_message):
        return self.llm_reply(user_message, self.config["system_prompts"]["word_definition"])

if __name__ == "__main__":
    # Load configuration file
    with open('config.json','r') as f:
        config = json.load(f)

    # Creat Directories if don't exist
    for key, path in config['paths'].items():
        os.makedirs(path, exist_ok=True)
    
    # Start the App
    app = App(config)
    app.root.mainloop()