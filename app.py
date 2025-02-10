from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox

import os, sys
import re, json

from mistralai import Mistral


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
    def __init__(self, parent, title = "Create Profile"):
        super().__init__(parent)
        self._title = title
        self.title(self._title)
        self.geometry('300x200')

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        tk.Label(self, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        submit_btn = tk.Button(self, text="Create Profile", command=self.create_profile)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        self.grid_rowconfigure(2, weight=1)
        
    def create_profile(self):
        name = self.name_entry.get()

        new_dir_path = Path(self.app.config['paths']['profiles'])/name
        if not new_dir_path.exists():
            new_dir_path.mkdir(parents=True)
            messagebox.showinfo('Success',f'Created Profile "{name}". ')
            self.destroy()
        else:
            messagebox.showerror('Error', f'Profile "{name}" already exists. ')
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