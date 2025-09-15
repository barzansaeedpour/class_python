import os
import time
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def read_datetime_from_file():
    """Open a file dialog and read datetime string from text file"""
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return

    try:
        ?????

        # Expected format: YYYY-MM-DD HH:MM
        target_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        action_time = target_time - timedelta(minutes=2)

        lbl_status.config(text=f"{action_var.get()} scheduled at: {action_time}")
        schedule_action(action_time, action_var.get())

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read datetime: {e}")

def schedule_action(action_time, action):
    """Start a background thread that waits until action_time"""
    def worker():
        while True:
            now = datetime.now()
            if now >= action_time:
                if action == "Hibernate":
                    os.system("shutdown /h")
                elif action == "Shutdown":
                    os.system("shutdown /s /t 0")
                elif action == "Sleep":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                break
            time.sleep(10)

    threading.Thread(target=worker, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Windows Scheduler")
root.geometry("420x220")

lbl_instructions = tk.Label(root, text="Select a text file with datetime (YYYY-MM-DD HH:MM):")
lbl_instructions.pack(pady=10)

btn_select = tk.Button(root, text="Select File", command=read_datetime_from_file)
btn_select.pack(pady=5)

# Action dropdown
lbl_action = tk.Label(root, text="Choose Action:")
lbl_action.pack(pady=5)

action_var = tk.StringVar(value="Hibernate")
action_menu = ttk.Combobox(root, textvariable=action_var, values=["Hibernate", "Shutdown", "Sleep"], state="readonly")
action_menu.pack(pady=5)

lbl_status = tk.Label(root, text="No schedule set yet.")
lbl_status.pack(pady=20)

root.mainloop()
