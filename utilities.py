import tkinter as tk
from tkinter import simpledialog

def add_language(languages):
    selected_languages = []

    def on_select():
        nonlocal selected_languages
        selected_indices = listbox.curselection()
        selected_languages = [languages[i] for i in selected_indices]
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Select Languages")
    dialog.geometry("300x500")
    dialog.rowconfigure(0, weight=1)
    dialog.columnconfigure(0, weight=1)
    listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
    listbox.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

    for lang in languages:
        listbox.insert(tk.END, lang)

    btn_select = tk.Button(dialog, text="Select", command=on_select)
    btn_select.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

    dialog.transient()  # Keep it on top of the main window
    dialog.grab_set()  # Make modal
    dialog.wait_window()

    return selected_languages


def get_contrast_color(hex_color):
    if hex_color is None:
        return "#000000"
    """Returns black or white for better contrast against the given background color."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 128 else "#FFFFFF" 