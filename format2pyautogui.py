# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:07:08 2019

@author: hoangt1
"""

# Convert mouse events to pyautogui format. Called in on_press()
def mouse2pyautogui(x = None, y = None, button = None, dx = None, dy = None):
    # example: mouse2pyautogui(x = x, y = y, button = button)
    # Mouse clicking
    if button:
        if str(button) == "Button.left":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'left')"
        elif str(button) == "Button.right":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'right')"
        elif str(button) == "Button.middle":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'middle')"

    # example: mouse2pyautogui(x = x, y = y, dx = dx, dy = dy)
    # Mouse vertical scrolling
    if dy: return f"pyautogui.scroll({dy}, x = {x}, y = {y})"

    # Mouse horizontal scrolling
    if dx: return f"pyautogui.hscroll({dx}, x = {x}, y = {y})"

# Convert keyboard events to pyautogui format. Called in on_press()
def keyboard2pyautogui(key_pressed = None, key_released = None):
    if key_pressed:
        return f"pyautogui.press({str(key_pressed)})"
        # for special keys (enter, tab, shift, ...) you need to compare each of them
        # because pynput and pyautogui name them differently. More here:
        # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.KeyCode
        # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys

#%%
def consolidate(recorded_data : list) -> list:
    print(recorded_data)
    for data in recorded_data:
        pass
    # Cleanup scrolling
    # Cleanup typewrite
    # Cleanup comments (start with shift + 3)
    # Distinguish between comments and string input
    # Cleanup combination keys. We might need to get key_released as well.

