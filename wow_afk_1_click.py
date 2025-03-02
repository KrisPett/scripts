import pyautogui
import time

if __name__ == "__main__":
    print("Pressing '1' every second...")
    while True:
        pyautogui.press('1')
        time.sleep(0.30)
