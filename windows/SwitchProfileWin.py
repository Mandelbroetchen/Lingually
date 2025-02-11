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

class SwitchProfileWin(Toplevel):
    def __init__(self, parent, title="Switch Profile"):
        super().__init__(parent)
        self._title = title
        self.title(self._title)
        self.geometry('480x320')

        padx, pady = 2, 2

        profiles_names = self.app.profile_names

        # Configure grid layout
        self.columnconfigure(0, weight=1)
        for i in range(len(profiles_names)):
            self.rowconfigure(i, weight=1)

        for index, name in enumerate(profiles_names):
            profile_info = self.app.get_profile_info(name)
            color = profile_info["color"]
            text_color = utilities.get_contrast_color(color)

            # Create button
            btn = tk.Button(
                self, text=name, bg=color, fg=text_color,
                font=("Arial", 14, "bold"), relief="raised",
                command=lambda n=name: self.switch_profile(n)
            )
            btn.grid(row=index, column=0, sticky="nsew", padx=padx, pady=pady)

    def switch_profile(self, name):
        """Sets the current profile in the app."""
        self.app.profile = name
        self.destroy()  # Close the window after switching