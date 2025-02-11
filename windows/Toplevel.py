from dotenv import load_dotenv
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, colorchooser
import langcodes
from mistralai import Mistral

import os, sys
import re, json

import utilities

class Toplevel(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transient()
        self.grab_set()
        self.focus()

    @property
    def app(self):
        try:
            return self.master.app
        except AttributeError:
            return self.master