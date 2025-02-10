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
    dialog.geometry("300x400")

    listbox = tk.Listbox(dialog, selectmode=tk.MULTIPLE)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    for lang in languages:
        listbox.insert(tk.END, lang)

    btn_select = tk.Button(dialog, text="OK", command=on_select)
    btn_select.pack(pady=10)

    dialog.transient()  # Keep it on top of the main window
    dialog.grab_set()  # Make modal
    dialog.wait_window()

    return selected_languages
