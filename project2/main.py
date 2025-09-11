import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# اتصال به دیتابیس
conn = sqlite3.connect("warehouse.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')
conn.commit()


def add_product():
    name = simpledialog.askstring("نام کالا", "نام کالا را وارد کنید:")
    if not name:
        return
    try:
        quantity = int(simpledialog.askstring("تعداد", "تعداد کالا را وارد کنید:"))
        price = float(simpledialog.askstring("قیمت", "قیمت کالا را وارد کنید:"))
    except:
        messagebox.showerror("خطا", "تعداد و قیمت باید عدد باشند.")
        return

    cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()
    messagebox.showinfo("موفقیت", f"{name} با موفقیت اضافه شد.")
    show_inventory()


def remove_product():
    pass


def search_product():
    pass


def show_inventory():
    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()
    update_tree(results)


def update_tree(data):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert("", "end", values=row)


# GUI
root = tk.Tk()
root.title("مدیریت انبار")
root.geometry("600x400")

# دکمه‌ها
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="افزودن کالا", command=add_product).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="حذف کالا", command=remove_product).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="جستجو", command=search_product).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="نمایش موجودی", command=show_inventory).grid(row=0, column=3, padx=5)

# جدول نمایش کالاها
columns = ("ID", "نام", "تعداد", "قیمت")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(expand=True, fill="both", pady=10)

show_inventory()
root.mainloop()
conn.close()
