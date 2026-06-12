import keyboard
import tkinter as tk
import json
from datetime import datetime
import os

def save_json(note_text):
    file_path = "notes.json"
    new_entry = {"note": note_text, "datetime": str(datetime.now())}
    
    if not os.path.exists(file_path):
        data = []
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    
    data.append(new_entry)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def show_notes():
    note_show = tk.Toplevel() 
    note_show.title("ALL NOTES")
    
    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            notes = json.load(f)
            text_area = tk.Text(note_show, height=10, width=40)
            text_area.pack()
            for n in notes:
                text_area.insert(tk.END, f"{n['datetime']} | {n['note']}\n")
    except (FileNotFoundError, json.JSONDecodeError):
        tk.Label(note_show, text="No notes found").pack()

def take_note_app():
    def save_and_close():
        save_json(note_entry.get())
        note_taker.destroy() 
    note_taker = tk.Toplevel() 
    note_taker.title("QUICK NOTE")

    note_entry = tk.Entry(note_taker, width=30)
    note_entry.pack(pady=10)

    tk.Button(note_taker, text="SAVE", command=save_and_close).pack()
    tk.Button(note_taker, text="SHOW NOTES", command=show_notes).pack()

root = tk.Tk()
root.withdraw()

keyboard.add_hotkey("ctrl+alt+n", take_note_app)
root.mainloop()