import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

HISTORY_FILE = "history.json"
history = []

def generate_password():
    length = length_var.get()

    if length < 4 or length > 50:
        messagebox.showerror("Error", "Длина должна быть между 4 и 50")
        return

    chars = ""

    if use_digits.get():
        chars += string.digits
    if use_letters.get():
        chars += string.ascii_letters
    if use_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Error", "Выберите хотя бы 1 тип символов")
        return

    password = ''.join(random.choice(chars) for _ in range(length))

    result_var.set(password)
    add_to_history(password)


def add_to_history(password):
    history.append(password)
    tree.insert("", tk.END, values=(password,))
    save_history()


def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f)
    except Exception as e:
        print("Ошибка сохранения:", e)

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)

            for pwd in history:
                tree.insert("", tk.END, values=(pwd,))
        except:
            history = []

root = tk.Tk()
root.title("Генератор паролей")
root.geometry("500x500")

tk.Label(root, text="Длина пароля:").pack()

length_var = tk.IntVar(value=12)
tk.Scale(root, from_=4, to=50, orient=tk.HORIZONTAL, variable=length_var).pack()

use_digits = tk.BooleanVar(value=True)
use_letters = tk.BooleanVar(value=True)
use_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Включать цифры: (0-9)", variable=use_digits).pack()
tk.Checkbutton(root, text="Включать буквы: (a-z A-Z)", variable=use_letters).pack()
tk.Checkbutton(root, text="Включать символы: (!@#...)", variable=use_symbols).pack()

tk.Button(root, text="Сгенерировать", command=generate_password).pack(pady=10)

result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, font=("Arial", 14), justify="center").pack(pady=10)

tk.Label(root, text="История:").pack()

tree = ttk.Treeview(root, columns=("password",), show="headings")
tree.heading("password", text="Сгенерированные пароли:")
tree.pack(expand=True, fill="both")

load_history()

root.mainloop()