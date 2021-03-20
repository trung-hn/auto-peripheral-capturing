import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Convert mouse events to pyautogui format. Called in on_press()


def mouse2pyautogui(x=None, y=None, button=None, dx=None, dy=None):
    # example: mouse2pyautogui(x = x, y = y, button = button)
    # Mouse clicking
    if button:
        if str(button) == "Button.left":
            return f"pyautogui.click({x}, {y}, duration=set_duration)"
        elif str(button) == "Button.right":
            return f"pyautogui.rightClick({x}, {y}, duration=set_duration)"
        elif str(button) == "Button.middle":
            return f"pyautogui.middleClick({x}, {y}, duration=set_duration)"

    # example: mouse2pyautogui(x = x, y = y, dx = dx, dy = dy)
    # Mouse vertical scrolling
    if dy:
        return f"pyautogui.scroll({dy}, x = {x}, y = {y})"

    # Mouse horizontal scrolling
    if dx:
        return f"pyautogui.hscroll({dx}, x = {x}, y = {y})"


# Convert keyboard events to pyautogui format. Called in on_press()
def keyboard2pyautogui(key_pressed=None, key_released=None):

    mapping = {'Key.space': 'space', 'Key.enter': 'enter', "Key.caps_lock": "capslock",
               "Key.backspace": "backspace", "Keys.down": "down", "Key.up": "up", "Key.left": "left",
               "Key.right": "right", "Key.page_down": "pagedown", "Key.page_up": "pageup",
               "Key.tab": "tab", "Key.delete": "delete"}
    key_pressed = str(key_pressed)
    if key_pressed in mapping:
        return f'pyautogui.press("{mapping[key_pressed]}")'

    elif len(key_pressed) == 1:
        return f'pyautogui.press({key_pressed})'
    return ''
    # for special keys (enter, tab, shift, ...) you need to compare each of them
    # because pynput and pyautogui name them differently. More here:
    # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.KeyCode
    # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys

    #                ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    # ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    # '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    # 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    # 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    # 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    # 'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    # 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    # 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    # 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    # 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    # 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    # 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    # 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    # 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    # 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    # 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    # 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    # 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    # 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    # 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    # 'command', 'option', 'optionleft', 'optionright']
    # clean up scroll statements as well


def img2pyautogui(save_image_path, save_image_name):
    image_code = f'{save_image_name} = r\'{save_image_path}\'\n' \
                 f'find_and_click_image({save_image_name})\n' \
                 f'sleep(1.5)\n\n'
    return image_code


# write recorded data to output file selected by user
def write_output_file(recorded_data: list, save_file_path: str, header_file_path=None) -> None:
    global dir_path
    with open(save_file_path, 'w') as fo:
        header_file_path = f'{dir_path}\header_py_auto.py'
        if header_file_path:
            print_header(fo, header_file_path)

        # clean up typewrite comments
        fo.write("\n".join(recorded_data))
    print(f"Data is saved at {save_file_path}")
    # Cleanup scrolling
    # Cleanup typewrite
    # Cleanup comments (start with shift + 3)
    # Distinguish between comments and string input
    # Cleanup combination keys. We might need to get key_released as well.


def print_header(file, header_file_path):
    with open(header_file_path, 'r') as header_file:
        for line in header_file.readlines():
            file.write(line)


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
