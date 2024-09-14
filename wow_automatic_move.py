import pyautogui
import time

def move_forward(duration):
    pyautogui.keyDown('w')
    time.sleep(duration)
    pyautogui.keyUp('w')

def turn_left(duration):
    pyautogui.keyDown('a')
    time.sleep(duration)
    pyautogui.keyUp('a')

def turn_right(duration):
    pyautogui.keyDown('d')
    time.sleep(duration)
    pyautogui.keyUp('d')

def jump(duration):
    pyautogui.press('space')
    time.sleep(duration)

def stop_movement():
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('d')

def detect_mouse_activity(initial_mouse_position, duration=0.1):
    time.sleep(duration)
    return pyautogui.position() != initial_mouse_position

if __name__ == "__main__":
    print("Starting movement in...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    while True:
        initial_mouse_position = pyautogui.position()

        for action, duration in [
            (move_forward, 3), 
            (jump, 0.5),
            (turn_left, 1), 
            (move_forward, 2), 
            (turn_right, 1)
        ]:
            action(duration)
            
            if detect_mouse_activity(initial_mouse_position):
                print("Mouse activity detected. Stopping movement...")
                stop_movement()
                break
        else:
            continue
        
        break

    print("Movement stopped.")
