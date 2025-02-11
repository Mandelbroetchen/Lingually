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

class SetModelWin(Toplevel):
    def __init__(self, parent, title="Create Profile"):
        super().__init__(parent)
        self._title = title
        self.title(self._title)
        self.geometry('480x320')
        padx, pady = 2, 2
        '''
        1. Use .grid() to add elements as shown in the table below
        2. All stickness = "nsew"
        3. Column 1 has weight = 1
        4. Use padx, pady as above
        5. The buttons on the last row should have the same size
        6. Dont implement functions of the button
        7. 

        | Modelname:                              | Dropdownmenu["mistral-large-latest", ...]   |
        | API key:                                | Entry                                       |
        | f'Tempreture({shows slidebar number}):' | Slidebar 0 to 2 step 0.1                    |
        | f'Maxtoken({shows slidebar number}):'   | Slidebar 1 to 100k logarithmically scalling |
        | Discard Button                          |Save Button                                  |
        '''
        self.columnconfigure(1, weight=1)
        
        # Model name dropdown
        ttk.Label(self, text="Model name:").grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(self, textvariable=self.model_var, values=["mistral-large-latest", "mistral-small", "custom-model"])
        self.model_dropdown.grid(row=0, column=1, sticky="nsew", padx=padx, pady=pady)
        
        # API Key entry
        ttk.Label(self, text="API key:").grid(row=1, column=0, sticky="nsew", padx=padx, pady=pady)
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(self, textvariable=self.api_key_var)
        self.api_key_entry.grid(row=1, column=1, sticky="nsew", padx=padx, pady=pady)
        
        # Temperature slider
        self.temperature_var = tk.DoubleVar(value=1.0)
        self.temperature_label = ttk.Label(self, text=f"Temperature({self.temperature_var.get():.1f}):")
        self.temperature_label.grid(row=2, column=0, sticky="nsew", padx=padx, pady=pady)
        self.temperature_slider = ttk.Scale(self, from_=0, to=20, orient="horizontal", variable=self.temperature_var, command=self.update_temperature_label)
        self.temperature_slider.bind("<ButtonRelease-1>", self.snap_temperature)
        self.temperature_slider.grid(row=2, column=1, sticky="nsew", padx=padx, pady=pady)

        # Max token slider (logarithmic scaling)
        self.token_var = tk.IntVar(value=1000)
        self.token_label = ttk.Label(self, text=f"Max Tokens({self.token_var.get()}):")
        self.token_label.grid(row=3, column=0, sticky="nsew", padx=padx, pady=pady)
        self.token_slider = ttk.Scale(self, from_=0, to=20, orient="horizontal", command=self.update_token_value)
        self.token_slider.bind("<ButtonRelease-1>", self.snap_token)
        self.token_slider.grid(row=3, column=1, sticky="nsew", padx=padx, pady=pady)

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=padx, pady=pady)
        
        self.discard_button = ttk.Button(self.button_frame, text="Discard")
        self.discard_button.grid(row=0, column=0, sticky="nsew", padx=padx, pady=pady)
        
        self.save_button = ttk.Button(self.button_frame, text="Save")
        self.save_button.grid(row=0, column=1, sticky="nsew", padx=padx, pady=pady)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

    def update_temperature_label(self, val):
        self.temperature_label.config(text=f"Temperature({float(val)/10:.1f}):")
    
    def update_token_value(self, val):
        token_value = int(2 ** float(val))  
        self.token_var.set(token_value)
        self.token_label.config(text=f"Max tokens({self.token_var.get()}):")

    def snap_temperature(self, event):
        val = round(self.temperature_var.get())  
        self.temperature_var.set(val)
        self.update_temperature_label(val)

    def snap_token(self, event):
        val = round(self.token_slider.get())  
        self.token_slider.set(val)
        self.update_token_value(val)


