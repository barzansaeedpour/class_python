# وارد کردن کتابخانه Tkinter برای ساخت رابط کاربری گرافیکی
import tkinter as tk
# وارد کردن ماژول‌های پیشرفته‌تر Tkinter شامل Progressbar، پنجره فایل و پیام‌های هشدار
from tkinter import ttk, filedialog, messagebox
# وارد کردن کتابخانه requests برای دانلود فایل از اینترنت
import requests
# وارد کردن threading برای اجرای دانلود در پس‌زمینه و جلوگیری از قفل شدن GUI
import threading
# وارد کردن os برای مدیریت مسیر فایل‌ها
import os

# تابع برای انتخاب پوشه ذخیره فایل
def browse_location():
    # باز کردن پنجره انتخاب پوشه
    folder = filedialog.askdirectory()
    # اگر پوشه انتخاب شد، مقدار آن را به متغیر save_path اختصاص می‌دهد
    if folder:
        save_path.set(folder)

# تابع شروع دانلود فایل از URL
def download_file():
    # گرفتن آدرس URL از ورودی کاربر
    url = url_entry.get()
    # گرفتن مسیر ذخیره از ورودی کاربر
    folder = save_path.get()
    
    # بررسی اینکه URL وارد شده باشد
    if not url:
        messagebox.showerror("Error", "Please enter a URL")  # نمایش پیام خطا
        return
    # بررسی اینکه مسیر ذخیره انتخاب شده باشد
    if not folder:
        messagebox.showerror("Error", "Please select save location")  # نمایش پیام خطا
        return
    
    # اجرای تابع دانلود در یک Thread جداگانه تا GUI هنگام دانلود قفل نشود
    threading.Thread(target=start_download, args=(url, folder), daemon=True).start()

# تابع اصلی دانلود فایل
def start_download(url, folder):
    try:
        # ارسال درخواست به URL با فعال کردن حالت stream برای دانلود تکه‌ای
        response = requests.get(url, stream=True)
        # گرفتن اندازه کل فایل از هدر پاسخ
        total_size = int(response.headers.get('content-length', 0))
        # تعیین نام فایل بر اساس آخرین بخش URL و مسیر انتخابی
        filename = os.path.join(folder, url.split('/')[-1])
        
        downloaded = 0  # مقدار دانلود شده تاکنون
        chunk_size = 1024  # اندازه هر بخش دانلود (1 کیلوبایت)
        
        # باز کردن فایل در حالت نوشتن باینری
        with open(filename, 'wb') as f:
            # حلقه برای خواندن تکه‌های داده و نوشتن در فایل
            for data in response.iter_content(chunk_size=chunk_size):
                downloaded += len(data)  # به‌روزرسانی مقدار دانلود شده
                f.write(data)  # نوشتن داده در فایل
                # محاسبه درصد پیشرفت دانلود
                progress = int(downloaded / total_size * 100)
                # بروزرسانی ProgressBar
                progress_bar['value'] = progress
                # بروزرسانی متن درصد پیشرفت
                progress_label.config(text=f"{progress}%")
                # به‌روزرسانی فوری GUI
                root.update_idletasks()
        
        # نمایش پیام موفقیت بعد از اتمام دانلود
        messagebox.showinfo("Success", f"Downloaded {filename}")
        # بازنشانی ProgressBar و متن
        progress_bar['value'] = 0
        progress_label.config(text="")
    except Exception as e:
        # نمایش پیام خطا در صورت بروز مشکل
        messagebox.showerror("Error", str(e))

# ================== بخش ساخت GUI ==================

# ایجاد پنجره اصلی
root = tk.Tk()
root.title("Python Download Manager")  # عنوان پنجره
root.geometry("550x250")  # اندازه پنجره
root.resizable(False, False)  # غیرقابل تغییر بودن اندازه پنجره
root.configure(bg="#f0f0f0")  # رنگ پس‌زمینه پنجره

# عنوان اصلی برنامه
tk.Label(root, text="Download Manager", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# ---------- بخش URL ----------
url_frame = tk.Frame(root, bg="#f0f0f0")  # ایجاد فریم برای URL
url_frame.pack(pady=5, padx=10, fill="x")
tk.Label(url_frame, text="File URL:", width=12, anchor="w", bg="#f0f0f0").pack(side=tk.LEFT)  # لیبل URL
url_entry = tk.Entry(url_frame, width=45, font=("Helvetica", 12))  # فیلد ورودی URL
url_entry.pack(side=tk.LEFT, padx=5)

# ---------- بخش محل ذخیره ----------
save_frame = tk.Frame(root, bg="#f0f0f0")  # ایجاد فریم برای محل ذخیره
save_frame.pack(pady=5, padx=10, fill="x")
tk.Label(save_frame, text="Save Location:", width=12, anchor="w", bg="#f0f0f0").pack(side=tk.LEFT)  # لیبل محل ذخیره
save_path = tk.StringVar()  # متغیر نگهدارنده مسیر ذخیره
tk.Entry(save_frame, textvariable=save_path, width=35, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)  # فیلد ورودی مسیر
tk.Button(save_frame, text="Browse", command=browse_location, bg="#4caf50", fg="white", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)  # دکمه انتخاب پوشه

# ---------- بخش Progress Bar ----------
progress_frame = tk.Frame(root, bg="#f0f0f0")  # فریم برای نوار پیشرفت
progress_frame.pack(pady=20)
progress_bar = ttk.Progressbar(progress_frame, length=450)  # نوار پیشرفت
progress_bar.pack()
progress_label = tk.Label(progress_frame, text="", font=("Helvetica", 10), bg="#f0f0f0")  # لیبل درصد پیشرفت
progress_label.pack()

# ---------- دکمه دانلود ----------
tk.Button(root, text="Download", command=download_file, bg="#2196f3", fg="white", font=("Helvetica", 12, "bold"), width=15).pack(pady=10)

# اجرای حلقه اصلی GUI
root.mainloop()
