import tkinter as tk
from tkinter import simpledialog, ttk
import random

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class ToggleTreeview(ttk.Treeview):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,selectmode="none",**kwargs)
        self.bind("<ButtonPress-1>", self.on_item_click)

    def on_item_click(self, event):
        item = self.identify_row(event.y)
        if item in self.selection():
            self.selection_remove(item)
        else:
            self.selection_add(item)
    

def add_language(languages):
    selected_languages = []

    def on_select():
        nonlocal selected_languages
        selected_languages = [tree.item(item, "values")[0] for item in tree.selection()]
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Select Languages")
    dialog.geometry("300x500")
    dialog.rowconfigure(0, weight=1)
    dialog.columnconfigure(0, weight=1)
    
    tree = ToggleTreeview(dialog, columns=("Language",), show="headings", height=10)
    tree.heading("Language", text="Languages")
    tree.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
    
    for lang in languages:
        tree.insert("", "end", values=(lang,))
    
    # Enable selection toggling without holding Control

    
    btn_select = tk.Button(dialog, text="Select", command=on_select)
    btn_select.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
    
    dialog.transient()  # Keep it on top of the main window
    dialog.grab_set()  # Make modal
    dialog.wait_window()
    
    return selected_languages

def get_contrast_color(hex_color):
    if hex_color is None:
        return "#000000"
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 128 else "#FFFFFF"
