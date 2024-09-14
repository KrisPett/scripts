import pyautogui
import time
import random
import numpy as np
from PIL import ImageGrab

def move_forward(duration):
    pyautogui.keyDown('w')
    end_time = time.time() + duration
    while time.time() < end_time:
        if random.random() < 0.1:
            jump(0.1)
        if random.random() < 0.1:
            quick_direction_change()
        time.sleep(0.1)
    pyautogui.keyUp('w')

def move_backward(duration):
    pyautogui.keyDown('s')
    end_time = time.time() + duration
    while time.time() < end_time:
        if random.random() < 0.1:
            quick_direction_change()
        time.sleep(0.1)
    pyautogui.keyUp('s')

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
    pyautogui.keyUp('s')

def detect_mouse_activity(initial_mouse_position, duration=0.1):
    time.sleep(duration)
    return pyautogui.position() != initial_mouse_position

def capture_screen_region(region):
    left, top, width, height = region
    right = left + width
    bottom = top + height
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return np.array(screenshot)

def detect_stuck(region, check_interval=0.5, max_checks=2, threshold=5):
    prev_capture = capture_screen_region(region)
    stuck_count = 0
    
    for _ in range(max_checks):
        time.sleep(check_interval)
        new_capture = capture_screen_region(region)
        
        if np.sum(np.abs(prev_capture - new_capture)) < threshold:
            stuck_count += 1
        else:
            stuck_count = 0
        
        prev_capture = new_capture

        if stuck_count >= max_checks:
            return True
        
    return False

def quick_direction_change():
    print("Quick direction change.")
    random.choice([turn_left, turn_right])(random.uniform(0.1, 0.3))
def change_direction():
    print("Character appears to be stuck. Changing direction...")
    
    new_direction = random.choice([
        (turn_left, random.uniform(0.3, 1)), 
        (turn_right, random.uniform(0.3, 1)),
        (jump, random.uniform(0.3, 0.7)), 
        (move_backward, random.uniform(0.5, 1.5)), 
    ])
    
    action, duration = new_direction
    action(duration)

if __name__ == "__main__":
    print("Starting movement in...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    region_to_monitor = (100, 100, 50, 50)

    while True:
        initial_mouse_position = pyautogui.position()

        actions = [
            (move_forward, random.uniform(1, 2)), 
            (turn_left, random.uniform(0.3, 1)), 
            (turn_right, random.uniform(0.3, 1)), 
        ]

        random.shuffle(actions)

        for action, duration in actions:
            action(duration)
            
            if detect_mouse_activity(initial_mouse_position):
                print("Mouse activity detected. Stopping movement...")
                stop_movement()
                break
            
            if detect_stuck(region_to_monitor):
                change_direction()

        else:
            continue
        
        break

    print("Movement stopped.")
