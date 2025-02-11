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

class App:
    def __init__(self, config, llm_client):
        self.llm_client = llm_client
        self.config = config
        self.root = tk.Tk()
        self.root.app = self
        self.profile = "Alex"

        self.root.title(self.name)
        self.root.geometry('640x480')
        icon_image = Image.open("icon.png")
        self.icon = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(True, self.icon)


        menu_bar = tk.Menu(self.root)



        # Profile Menu
        profile_menu = tk.Menu(menu_bar, tearoff=0)
        profile_menu.add_command(label="New profile", command=lambda: CreateProfileWin(self.root))
        profile_menu.add_command(label="Switch profile*")
        profile_menu.add_command(label="Manage profiles*")

        menu_bar.add_cascade(label="Profile", menu=profile_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add word", command=lambda: AddWordWin(self.root))
        edit_menu.add_command(label="Add words from paragraph*")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Settings Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Set API key*")
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
    
    @property
    def profile_info(self):
        path = Path(self.config["paths"]["profiles"])/self.profile/"info.json"
        if path.exists():
            with open(str(path),'r') as f:
                info = json.load(f)
            return info
        else:
            return None
    
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
        messeges = [
            {"role": "system", "content": msg} for msg in system_messages
        ] + [{"role": "user", "content": user_message}]
        print(messeges)
        chat_response = self.llm_client.chat.complete(
            model=self.config["model"],
            messages=messeges,
            temperature=0
        ).choices[0].message.content
        return chat_response

    def llm_simple_reply(self, user_message):
        return self.llm_reply(user_message, self.config["system_prompts"]["simple_reply"])
    
    def llm_word_definition(self, user_message):
        return self.llm_reply(user_message, self.config["system_prompts"]["word_definition"])

if __name__ == "__main__":
    # Load LLM client
    load_dotenv()
    api_key = os.getenv("API_KEY")
    print(api_key)
    llm_client = Mistral(api_key)

    # Load configuration file
    with open('config.json','r') as f:
        config = json.load(f)

    # Creat Directories if don't exist
    for key, path in config['paths'].items():
        os.makedirs(path, exist_ok=True)
    
    # Start the App
    app = App(config, llm_client)
    app.root.mainloop()

'''chat_response = client.chat.complete(
    model=model,
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ],
    temperature=0
).choices[0].message.content'''