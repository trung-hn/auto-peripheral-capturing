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
import tkinter.filedialog as tk_dialog
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
def NamingGUI():
   naming_root = tk.Toplevel()
   naming_root.wm_title("Give me a name!!")

   # First Line
   tk.Label(naming_root, text = "Name of variable: ")\
           .grid(row = 0, column = 0, sticky = tk.W)

   variable_name = tk.StringVar()
   tk.Entry(naming_root, textvariable = variable_name, width = 30)\
           .grid(row = 0, column = 1)

   # Second Line
   tk.Button(naming_root, text = "Pick this name", command = naming_root.destroy)\
           .grid(row = 1, column = 0, columnspan = 2)


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
                  command = self.call_program, fg = "white",bg = "green", \
                  height = 1, width = 20).grid(row = 15, column = 0, columnspan = 2)
        
        self.save_as_button = tk.Button(root, text = "Save as", command = self.save_as,\
                  state = tk.DISABLED, height = 1, width = 10)
        self.save_as_button.grid(row = 15, column = 2, columnspan = 1)

        # Fourth line
        tk.Label(root, text = "Note:\n"
                 "Press L-Shift to Select Top Left Corner of Image\n"
                 "Press L-Ctrl to Select Bottom Right Corner of Image and Save\n",\
                 justify = tk.LEFT).grid(row = 20, column = 0, columnspan = 3, sticky = tk.W)

    def call_program(self):
        self.recorded_data = start_program(self.root)
        # By now, the program already stopped

        # Change state of save_as_button
        self.save_as_button.config(state = "normal")
        # Bring window to the front
        root.attributes('-topmost', 1)
        root.attributes('-topmost', 0)

    def save_as(self):
        # Prompt user for file path
        file_path = tk_dialog.asksaveasfilename(defaultextension=".py")
        # Write to file
        with open(file_path, "w") as f:
            f.write("import pyautogui\n\n")
            for data in self.recorded_data:
                f.write(data + "\n")

# Main program, this is the recorder
def start_program(root):
    # Controller
    mouse = MouseController()
    keyboard = KeyboardController()

    # Set up variable
    dir_path = os.path.dirname(os.path.realpath(__file__))
    mouse_top_left_corner = ()
    count = 0
    recorded_data = []
    recording = naming = False

    # Key pressed event
    def on_press(key):
        nonlocal mouse_top_left_corner, count, recording, naming
        # Record Image top-left pos
        if key == Key.shift:
            print(f"Top left image location: {mouse.position}")
            mouse_top_left_corner = mouse.position

        # Record Image bot-right pos
        elif False and key == Key.ctrl_l and mouse_top_left_corner:
            print(f"Image captured from {mouse_top_left_corner} to\
                {mouse.position} is save as screen_shot_{count}.png")
            end = [mouse.position[i] - mouse_top_left_corner[i] for i in range(2)]
            pyautogui.screenshot(region=(*mouse_top_left_corner, *end))\
                .save(f"{dir_path}/images/screen_shot_{count}.png")
            mouse_top_left_corner = ()
            count += 1

        # Start Recording
        elif key == Key.scroll_lock:
            print("Start Recording" if not recording else "Stop Recording")
            recording = not recording

        # Start Naming
        # Notice: if we want to record keyboard keystrokes, we will need to
        # turn off recording while naming so we can interact with naming GUI
        # without recoding those actions
        elif key == Key.num_lock:
            print("Start Naming" if not naming else "Stop Naming")
            naming = not naming

        # Stop Listener
        elif key == Key.esc:
            print("Stop program")
            return False
        # Record other keys
        elif recording:
            recorded_data.append(keyboard2pyautogui(key_pressed = key))
            print(keyboard2pyautogui(key_pressed = key))

    # Key released event
    def on_release(key):
        pass

    # Mouse moved event
    def on_move(x, y):
        pass
    
    # Mouse clicked event
    def on_click(x, y, button, pressed):
        if pressed and recording:
            if naming:
                print("Not Implemented")
                return
                # problem might be because of the blocking behavior of listeners
                naming_root = tk.Tk()
                NamingGUI(naming_root)
                naming_root.mainloop()
                global variable_name
                print(f"Mouse clicked at {x}, {y} with {button} is named {variable_name}")
            else:
                recorded_data.append(mouse2pyautogui(x = x, y = y, button = button))
                print(mouse2pyautogui(x = x, y = y, button = button))

    # Mouse scrolled event
    def on_scroll(x, y, dx, dy):
        if recording:
            recorded_data.append(mouse2pyautogui(x = x, y = y, dx = dx, dy = dy))
            print(mouse2pyautogui(x = x, y = y, dx = dx, dy = dy))

    # Start listening
    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    # return recorded data to run_program inside Main App Class to save
    return recorded_data

# Convert mouse events to pyautogui format
def mouse2pyautogui(x = None, y = None, button = None, dx = None, dy = None):
    # Mouse clicking
    if button:
        if str(button) == "Button.left":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'left')"
        elif str(button) == "Button.right":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'right')"
        elif str(button) == "Button.middle":
            return f"pyautogui.click(x = {x}, y = {y}, button = 'middle')"

    # Mouse vertical scrolling
    if dy: return f"pyautogui.scroll({dy}, x = {x}, y = {y})"

    # Mouse horizontal scrolling
    if dx: return f"pyautogui.hscroll({dx}, x = {x}, y = {y})"

# Convert keyboard events to pyautogui format
def keyboard2pyautogui(key_pressed = None):
    if key_pressed:
        return f"pyautogui.press({str(key_pressed)})"
        # for special keys (enter, tab, shift, ...) you need to compare each of them 
        # because pynput and pyautogui name them differently. More here:
        # https://pynput.readthedocs.io/en/latest/keyboard.html#pynput.keyboard.KeyCode
        # https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)#.pack(side="top", fill="both")
    root.mainloop()

