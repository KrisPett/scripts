import pyautogui
import math
import time
from pynput.mouse import Listener

RADIUS = 4
STEPS = 4
DELAY = 0.0000001

stop_flag = False

def on_click(x, y, button, pressed):
    global stop_flag
    if pressed:
        stop_flag = True
        return False

def move_in_circle(radius, steps, delay):
    global stop_flag
    while not stop_flag:
        current_x, current_y = pyautogui.position()

        for i in range(steps):
            if stop_flag:
                break

            angle = 2 * math.pi * i / steps

            x = current_x + radius * math.cos(angle)
            y = current_y + radius * math.sin(angle)

            pyautogui.moveTo(x, y)

            time.sleep(delay)

def main():
    with Listener(on_click=on_click) as listener:
        move_in_circle(RADIUS, STEPS, DELAY)

        listener.join()

    print("Program stopped by mouse click.")

if __name__ == "__main__":
    main()

