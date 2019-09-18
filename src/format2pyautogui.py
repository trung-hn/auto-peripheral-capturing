# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:07:08 2019

@author: hoangt1
"""
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Convert mouse events to pyautogui format. Called in on_press()
def mouse2pyautogui(x=None, y=None, button=None, dx=None, dy=None):
    # example: mouse2pyautogui(x = x, y = y, button = button)
    # Mouse clicking
    if button:
        if str(button) == "Button.left":
            return f"click({x}, {y}, duration=.25 )"
        elif str(button) == "Button.right":
            return f"rightClick({x}, {y}, duration=.25 )"
        elif str(button) == "Button.middle":
            return f"middleClick({x}, {y}, duration=.25 )"

    # example: mouse2pyautogui(x = x, y = y, dx = dx, dy = dy)
    # Mouse vertical scrolling
    if dy: return f"pyautogui.scroll({dy}, x = {x}, y = {y})"

    # Mouse horizontal scrolling
    if dx: return f"pyautogui.hscroll({dx}, x = {x}, y = {y})"


# Convert keyboard events to pyautogui format. Called in on_press()
def keyboard2pyautogui(key_pressed=None, key_released=None):
    if key_pressed:
        return f'typewrite({key_pressed})'
        # for special keys (enter, tab, shift, ...) you need to compare each of them
        # because pynput and pyautogui name them differently. More here:
        # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.KeyCode
        # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys


def img2pyautogui(save_image_path, save_image_name):
    image_code = f'{save_image_name} = r\'{save_image_path}\'\n'\
                 f'select({save_image_name})\n'\
                 f'sleep(1.5)\n\n'
    return image_code


# write recorded data to output file selected by user
def write_output_file(recorded_data: list, save_file_path: str, header_file_path=None) -> None:
    global dir_path
    print(recorded_data)
    with open(save_file_path, 'w') as file:
        header_file_path = f'{dir_path}\header_py_auto.py'
        if header_file_path:
            print_header(file, header_file_path)

        # clean up typewrite comments
        consolidate_typewrite(file, recorded_data)
    # Cleanup scrolling
    # Cleanup typewrite
    # Cleanup comments (start with shift + 3)
    # Distinguish between comments and string input
    # Cleanup combination keys. We might need to get key_released as well.


def print_header(file, header_file_path):
    with open(header_file_path, 'r') as header_file:
        for line in header_file:
            file.write(line)


# consolidate_typewrite statements from single letter to readable strings
def consolidate_typewrite(file, recorded_data):
    # during consolidating, the last line shouldn't be typewrite
    recorded_data.append('### end of buffer###')

    # clean up scroll statements as well
    typewrite_content = ''
    for line in recorded_data:
        if 'typewrite' in line:
            if 'Key.space' in line:
                typewrite_content += ' '
            if 'Key.backspace' in line:
                typewrite_content = typewrite_content[:-1]
            if len(line) == 15:
                letter = line[11:12]
                typewrite_content += letter
        else:
            if typewrite_content:
                if typewrite_content[0] != '`':
                    typewrite_statement = f'typewrite(\'{typewrite_content}\')\n'
                else:
                    typewrite_statement = '# ' + typewrite_content
                file.write(typewrite_statement)
                typewrite_content = ''
            file.write(line)

# TODO Function that calls write_output_file should include the

# first, request file name and display default path that it will be saved to
# include option for import header

'''
# User Notes
take pictures so that  the top left corner is where you want to click

to write a comment:
start the line with `
nobody ever uses the thing under tilda..
after you are done with the comment, CTRL+A to overwrite the text if you want to enter real text.

# Possible improvements
you could write a dictionary for shift+numbers for capitals and 
read the \n as an enter
'''
