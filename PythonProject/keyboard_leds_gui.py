import tkinter as tk
from tkinter import messagebox
import keyboard
import time
import threading

# Функція для миготіння вибраних клавіш
def blink_keys():
    keys = entry_keys.get()  # Отримуємо список клавіш з поля вводу
    delay = float(entry_delay.get())  # Отримуємо затримку
    repeats = int(entry_repeats.get())  # Отримуємо кількість повторень

    if keys.lower() == "all":
        keys = keyboard.all_modifiers  # Вибираємо всі клавіші-модифікатори (Ctrl, Alt, Shift тощо)
    else:
        keys = keys.split()  # Розбиваємо текст на список клавіш

    for _ in range(repeats):
        for key in keys:
            keyboard.press(key)  # Увімкнення клавіші
        time.sleep(delay)
        for key in keys:
            keyboard.release(key)  # Вимкнення клавіші
        time.sleep(delay)

    messagebox.showinfo("Готово!", "Миготіння клавіш завершено!")

# Функція для запуску миготіння в окремому потоці
def start_blinking():
    thread = threading.Thread(target=blink_keys)
    thread.start()

# Створюємо головне вікно
root = tk.Tk()
root.title("Миготіння клавіш")  # Назва вікна
root.geometry("300x200")  # Розмір вікна

# Текст та поля вводу
tk.Label(root, text="Клавіші (розділяти пробілом):").pack()
entry_keys = tk.Entry(root)
entry_keys.pack()

tk.Label(root, text="Затримка (секунди):").pack()
entry_delay = tk.Entry(root)
entry_delay.pack()

tk.Label(root, text="Кількість повторень:").pack()
entry_repeats = tk.Entry(root)
entry_repeats.pack()

# Кнопка запуску
start_button = tk.Button(root, text="Запустити", command=start_blinking)
start_button.pack()

# Запуск головного циклу вікна
root.mainloop()
