import keyboard
import tkinter as tk
import json
from datetime import datetime
import os
import pystray
from PIL import Image
import threading
from tkinter import ttk

image = Image.open("notes.png")

def after_click(icon, query):
    if str(query) == "Open App":
        take_note_app()
    elif str(query) == "Exit":
        icon.stop()
        root.quit()
        quit()

def load_json():
    file_path = "notes.json"
    
    if not os.path.exists(file_path):
        return []
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, list):
                return data
            else:
                return []
                
    except (json.JSONDecodeError, IOError):

        return []

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
    note_show.title("Your Notes")
    
    columns = ('date', 'note')
    tree = ttk.Treeview(note_show, columns=columns, show='headings')
    
    tree.heading('date', text='Ημερομηνία')
    tree.heading('note', text='Σημείωση')
    
    tree.column('date', width=150)
    tree.column('note', width=300)
    
    notes = load_json() 
    for n in notes:
        tree.insert('', tk.END, values=(n['datetime'][:16], n['note']))
        
    tree.pack(fill=tk.BOTH, expand=True)

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

    tk.Label(note_taker,text="Note icons created by Freepik - Flaticon").pack()

def setup_tray():
    image = Image.open("notes.png")
    icon = pystray.Icon("Note Taker", image, "Note Taker", 
                        menu=pystray.Menu(
                            pystray.MenuItem("Open App", lambda: root.after(0, take_note_app)),
                            pystray.MenuItem("Exit", lambda icon: (icon.stop(), root.quit()))
                        ))
    icon.run()

tray_thread = threading.Thread(target=setup_tray, daemon=True)
tray_thread.start()

root = tk.Tk()
root.withdraw()

keyboard.add_hotkey("ctrl+alt+n", lambda: take_note_app())
root.mainloop()