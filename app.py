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

        self.root.title(self.name)
        self.root.geometry('300x200')

        if len(self.profiles_names) == 0:
            print(self.profiles_names)
            create_profile = CreateProfile(self.root)
            create_profile.focus_set()

    @property
    def name(self):
        return self.config['name']

    @property
    def profiles_names(self):
        profiles_path = Path(self.config['paths']['profiles'])
        profiles_names = [dir.name for dir in profiles_path.iterdir() if dir.is_dir()]
        return profiles_names
    
class CreateProfile(tk.Toplevel):
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

        tk.Label(self, text="Email:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        submit_btn = tk.Button(self, text="Create Profile", command=self.create_profile)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        self.grid_rowconfigure(2, weight=1)
        
    def create_profile(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        
        if not name or not email:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Process profile creation (e.g., store in a database or file)
        messagebox.showinfo("Success", f"Profile Created!\nName: {name}\nEmail: {email}")
        self.destroy()  # Close the window



if __name__ == "__main__":
    # Load LLM client
    load_dotenv()
    api_key = os.getenv("API_KEY")
    llm = Mistral(api_key)

    # Load configuration file
    with open('config.json','r') as f:
        config = json.load(f)
    
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