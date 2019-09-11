# Date: 9/11/2019
# File: peripheral_capture.py
# Name: Trung Hoang
# Desc: Contact Paxton Wills for more info

from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
#import keyboard
import pyautogui, os
import tkinter as tk

global Variable_Name

# Popup GUI for naming
class NamingGUI(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Title
        self.root.title("Give me a name!!")

        # Bring window to the front
        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

        # Run naming_gui
        self.naming_gui()

    def naming_gui(self):
        naming_root = self.root
        # First Line
        tk.Label(naming_root, text = "Name of variable: ")\
                .grid(row = 0, column = 0, sticky = tk.W)

        self.variable_name = tk.StringVar()
        tk.Entry(naming_root, textvariable = self.variable_name, width = 30)\
                .grid(row = 0, column = 1)
        # Second Line
        tk.Button(naming_root, text = "Pick this name", command = self.assign_var_to_global)\
                .grid(row = 1, column = 0, columnspan = 2)

    def assign_var_to_global(self):
        global variable_name
        variable_name = self.variable_name.get()

# Not implemented
#def NamingGUI():
#    naming_root = tk.Toplevel()
#    naming_root.wm_title("Give me a name!!")
#
#    # First Line
#    tk.Label(naming_root, text = "Name of variable: ")\
#            .grid(row = 0, column = 0, sticky = tk.W)
#
#    variable_name = tk.StringVar()
#    tk.Entry(naming_root, textvariable = variable_name, width = 30)\
#            .grid(row = 0, column = 1)
#
#    # Second Line
#    tk.Button(naming_root, text = "Pick this name", command = naming_root.destroy)\
#            .grid(row = 1, column = 0, columnspan = 2)


# Main GUI
class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        # Title
        self.root.title("Super Recorder")

        # Bring window to the front
        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

        # Run main_gui
        self.main_gui()

    def main_gui(self):
        root = self.root

        # First Line
        tk.Label(root, text = "Press this key to start recording:")\
                .grid(row = 0, column = 0, sticky = tk.W)

        recording_button = tk.StringVar(root)
        recording_button.set("Scroll Lock")
        choices = {"Scroll Lock"}
        recording_button_option = tk.OptionMenu(root, recording_button, *choices)
        recording_button_option.grid(row = 0, column = 2)

        # Second line
        tk.Label(root, text = "Press this key to start naming:")\
                .grid(row = 1, column = 0, sticky = tk.W)

        naming_button = tk.StringVar(root)
        naming_button.set("Num Lock")
        choices = {"Num Lock"}
        naming_button_option = tk.OptionMenu(root, naming_button, *choices)
        naming_button_option.grid(row = 1, column = 2)

        # Third line
        tk.Button(root, text = "Start (press Esc to stop)", \
                  command = lambda: start_program(root), fg = "white",bg = "green", \
                  height = 1, width = 20).grid(row = 15, column = 0, columnspan = 3)
        # Fourth line
        tk.Label(root, text = "Note:\n"
                 "Press L-Shift to Select Top Left Corner of Image\n"
                 "Press L-Ctrl to Select Bottom Right Corner of Image and Save\n",\
                 justify = tk.LEFT).grid(row = 20, column = 0, columnspan = 3, sticky = tk.W)

# Main program, this is the recorder
def start_program(root):
    mouse = MouseController()
    keyboard = KeyboardController()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    start = ()
    count = 0
    recording = naming = False

    # --------------KEYBOARD----------
    def on_press(key):
        nonlocal start, count, recording, naming
#        print(f'-----DEBUG-----: {key} pressed')

        # Record Image pos top-left
        if key == Key.shift:
            print(f"Top left image location: {mouse.position}")
            start = mouse.position

        # Record Image pos bot-right
        elif key == Key.ctrl_l and start:
            print(f"""Image captured from {start} to {mouse.position} is save as screen_shot_{count}.png""")
            end = [mouse.position[i] - start[i] for i in range(2)]
            pyautogui.screenshot(region=(*start, *end)).save(f"{dir_path}/images/screen_shot_{count}.png")
            start = ()
            count += 1

        # Recording
        elif key == Key.scroll_lock:
            print("Start Recording" if not recording else "Stop Recording")
            recording = not recording

        # Naming
        # Notice: if we want to record keyboard keystrokes, we will need to
        # turn off recording while naming so we can interact with naming GUI
        # without recoding those actions
        elif key == Key.num_lock:
            print("Not Implemented")
            return
            print("Start Naming" if not naming else "Stop Naming")
            naming = not naming

        # Stop Listener = Exit
        elif key == Key.esc:
            print("Stop program")
            return False

    def on_release(key):
        pass

    # --------------MOUSE-------------
    def on_move(x, y):
        pass

    def on_click(x, y, button, pressed):
        if pressed and recording:
            if naming:
                # problem might be because of the blocking behavior of listeners
                naming_root = tk.Tk()
                NamingGUI(naming_root)
                naming_root.mainloop()
                global variable_name
                print(f"Mouse clicked at {x}, {y} with {button} is named {variable_name}")
            else:
                print(convert2pyautogui(x = x, y = y, button = button))
#                print(f"Mouse clicked at {x}, {y} with {button}")

    def on_scroll(x, y, dx, dy):
        if recording:
            print(convert2pyautogui(x = x, y = y, dx = dx, dy = dy))
#            print(f"Mouse scrolled at {x}, {y}, {dx}, {dy}")

    # Turn off scroll lock and num lock at the beginning of each run
#    if KeyboardReader.is_pressed("scroll_lock"):
#        keyboard.press(Key.num_lock)
#        keyboard.release(Key.num_lock)
#    if Key.scroll_lock:
#        keyboard.press(Key.scroll_lock)
#        keyboard.release(Key.scroll_lock)

    # Start listening
    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    # Bring window to the front after listening
    root.attributes('-topmost', 1)
    root.attributes('-topmost', 0)

def convert2pyautogui(x = None, y = None, button = None, dx = None, dy = None):
    # Mouse clicking
    if button:
        if str(button) == "Button.left":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'left')"
        elif str(button) == "Button.right":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'right')"
        elif str(button) == "Button.middle":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'middle')"

    # Mouse vert scrolling
    if dy: return f"pyautogui.scroll({dy}, x = {x}, y = {y})"

    # Mouse hori scrolling
    if dx: return f"pyautogui.hscroll({dx}, x = {x}, y = {y})"


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)#.pack(side="top", fill="both")
    root.mainloop()

