import ctypes
import time
import logging

# Логування активності
logging.basicConfig(filename="keyboard_leds.log", level=logging.INFO, format="%(asctime)s - %(message)s",
                    encoding="utf-8")

# Windows API
user32 = ctypes.windll.user32

# Повний список клавіш Windows (VK-коди)
VK_CODES = {
    "ESC": 0x1B, "TAB": 0x09, "CAPSLOCK": 0x14, "SHIFT": 0x10, "CTRL": 0x11, "ALT": 0x12,
    "SPACE": 0x20, "ENTER": 0x0D, "BACKSPACE": 0x08, "DELETE": 0x2E, "INSERT": 0x2D,
    "HOME": 0x24, "END": 0x23, "PAGEUP": 0x21, "PAGEDOWN": 0x22,
    "LEFT": 0x25, "UP": 0x26, "RIGHT": 0x27, "DOWN": 0x28,
    "NUMLOCK": 0x90, "SCROLLLOCK": 0x91, "PRINTSCREEN": 0x2C, "PAUSE": 0x13,
    "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74, "F6": 0x75, "F7": 0x76,
    "F8": 0x77, "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B,
    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37,
    "8": 0x38, "9": 0x39,
    "A": 0x41, "B": 0x42, "C": 0x43, "D": 0x44, "E": 0x45, "F": 0x46, "G": 0x47, "H": 0x48,
    "I": 0x49, "J": 0x4A, "K": 0x4B, "L": 0x4C, "M": 0x4D, "N": 0x4E, "O": 0x4F, "P": 0x50,
    "Q": 0x51, "R": 0x52, "S": 0x53, "T": 0x54, "U": 0x55, "V": 0x56, "W": 0x57, "X": 0x58,
    "Y": 0x59, "Z": 0x5A,
    "-": 0xBD, "=": 0xBB, "[": 0xDB, "]": 0xDD, ";": 0xBA, "'": 0xDE, ",": 0xBC, ".": 0xBE, "/": 0xBF,
    "\\": 0xDC, "`": 0xC0
}


def toggle_led(key, state):
    """Змінює стан клавіші (індикатора)"""
    if key in VK_CODES:
        vk_code = VK_CODES[key]
        if state:
            user32.keybd_event(vk_code, 0, 0, 0)
            user32.keybd_event(vk_code, 0, 2, 0)
        else:
            user32.keybd_event(vk_code, 0, 0, 0)
            user32.keybd_event(vk_code, 0, 2, 0)


def block_input(state):
    """Блокує або розблокує введення"""
    user32.BlockInput(state)


def blink_keys(keys, delay, times):
    """Мигання вибраних клавіш із блокуванням введення"""
    block_input(True)  # Блокуємо введення
    print("⚠ Введення тимчасово вимкнене, зачекайте...")

    for _ in range(times):
        for key in keys:
            toggle_led(key, True)
        time.sleep(delay)
        for key in keys:
            toggle_led(key, False)
        time.sleep(delay)

    block_input(False)  # Розблокуємо введення
    print("✅ Введення знову увімкнене.")

    logging.info(f"Мигали клавіші: {', '.join(keys)} | {times} раз(ів), затримка {delay} сек.")


def main():
    print("Введіть клавіші, які повинні мигати (наприклад, 'F4 K AltGr Q . TAB -') або 'all' для всіх клавіш:")
    selected_keys = input("Ваш вибір: ").strip().upper().split()

    if "ALL" in selected_keys:
        chosen_keys = list(VK_CODES.keys())  # Вибір усіх клавіш
    else:
        chosen_keys = [key for key in selected_keys if key in VK_CODES]

    if not chosen_keys:
        print("Помилка: виберіть хоча б одну клавішу!")
        return

    try:
        delay = float(input("Введіть затримку між миганнями (у секундах): "))
        times = int(input("Скільки разів мигати?: "))
    except ValueError:
        print("Помилка: введіть число!")
        return

    blink_keys(chosen_keys, delay, times)


if __name__ == "__main__":
    main()
