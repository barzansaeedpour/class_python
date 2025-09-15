import os
import time
import threading
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import filedialog, ttk

# Global variable to store the datetime string from file
target_datetime_str = None

def select_file():
    """Open a file dialog and store datetime string"""
    global target_datetime_str
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    try:
        ??????
            
        lbl_file.config(text=f"Selected file: {filepath.split('/')[-1]}")
        lbl_confirm.config(text="")  # Clear previous confirmation
    except Exception as e:
        lbl_file.config(text=f"Error reading file: {e}")

def submit_schedule():
    """Schedule the action based on selected options and file"""
    global target_datetime_str
    if not target_datetime_str:
        lbl_status.config(text="No file selected!")
        return
    try:
        # Parse datetime from file
        target_time = datetime.strptime(target_datetime_str, "%Y-%m-%d %H:%M")
        
        # Get minutes before from input
        try:
            minutes_before = int(minutes_var.get())
        except ValueError:
            minutes_before = 2
        
        action_time = target_time - timedelta(minutes=minutes_before)
        
        # Show confirmation text inside the app
        lbl_confirm.config(
            text=f"✅ {action_var.get()} scheduled at: {action_time.strftime('%Y-%m-%d %H:%M')}"
        )

        # Update status
        lbl_status.config(text="Schedule set successfully!")

        schedule_action(action_time, action_var.get())
        
    except Exception as e:
        lbl_status.config(text=f"Error: {e}")

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
root.geometry("450x320")

lbl_instructions = tk.Label(root, text="Select a text file with datetime (YYYY-MM-DD HH:MM):")
lbl_instructions.pack(pady=10)

btn_select = tk.Button(root, text="Select File", command=select_file)
btn_select.pack(pady=5)

lbl_file = tk.Label(root, text="No file selected.")
lbl_file.pack(pady=5)

# Action dropdown
lbl_action = tk.Label(root, text="Choose Action:")
lbl_action.pack(pady=5)

action_var = tk.StringVar(value="Hibernate")
action_menu = ttk.Combobox(root, textvariable=action_var, values=["Hibernate", "Shutdown", "Sleep"], state="readonly")
action_menu.pack(pady=5)

# Minutes before input
lbl_minutes = tk.Label(root, text="Minutes before scheduled time:")
lbl_minutes.pack(pady=5)

minutes_var = tk.StringVar(value="2")
entry_minutes = tk.Entry(root, textvariable=minutes_var, width=5)
entry_minutes.pack(pady=5)

# Submit button
btn_submit = tk.Button(root, text="Submit", command=submit_schedule)
btn_submit.pack(pady=10)

# Confirmation label
lbl_confirm = tk.Label(root, text="", fg="green", font=("Arial", 12, "bold"))
lbl_confirm.pack(pady=5)

lbl_status = tk.Label(root, text="No schedule set yet.")
lbl_status.pack(pady=5)

root.mainloop()
