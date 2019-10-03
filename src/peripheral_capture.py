# Date: 9/11/2019
# File: peripheral_capture.py
# Name: Trung Hoang
# Desc: Contact Paxton Wills for more info

from pynput.mouse import Listener as MouseListener
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from format2pyautogui import mouse2pyautogui, keyboard2pyautogui, img2pyautogui, write_output_file
# import keyboard
import pyautogui, os, threading, webbrowser
import tkinter as tk
import tkinter.filedialog as tk_dialog


# Main GUI
class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        # Init variables
        self.root = root
        self.button_map = dict()
        self.recorded_data = []
        self.img_trigger_key = tk.StringVar(root)
        self.recording_trigger_key = tk.StringVar(root)
        self.file_path = ""
        self.message = None

        self.root.title("Super Recorder")
        # Bring window to the front
        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

        self.main_gui()

    def main_gui(self):
        root = self.root

        # Recording Options
        tk.Label(root, text="Press this key to start recording:").grid(row=0, column=0, sticky=tk.W)
        self.recording_trigger_key.set("Scroll Lock")
        choices = {"None", "Scroll Lock", "Num Lock", "Caps Lock"}
        tk.OptionMenu(root, self.recording_trigger_key, *choices).grid(row=0, column=1)

        # Image Capturing Options
        tk.Label(root, text="Press this key to start Image capturing:").grid(row=2, column=0, sticky=tk.W)
        self.img_trigger_key.set("Num Lock")
        choices = {"None", "Scroll Lock", "Num Lock", "Caps Lock"}
        tk.OptionMenu(root, self.img_trigger_key, *choices).grid(row=2, column=1)

        # Start button
        start_button = tk.Button(root, text="Choose Save Location and Start Program", command=self.call_program,
                                 fg="white", bg="green", height=2, width=30, cursor="hand2").grid(row=15, column=0,
                                                                                                  columnspan=2)

        # Note
        tk.Label(root, text="Note:\n"
                            "Press L-Shift to Select Top Left Corner of Image\n"
                            "Press L-Ctrl to Select Bottom Right Corner of Image and Save\n"
                            "Images will be saved in the same folder as script file.",
                 justify=tk.LEFT).grid(row=20, column=0, columnspan=1, sticky=tk.W)

        # Message
        self.message = tk.Label(root, text="...", fg="white", bg="green", justify=tk.LEFT)
        self.message.grid(row=30, column=0, columnspan=3, sticky="ew", )

        # Credit
        link1 = tk.Label(root, text="Credit: Trung Hoang", fg="blue", cursor="hand2")
        link1.grid(row=40, column=0, columnspan=1, sticky="e")
        link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/trung-hn"))

        link1 = tk.Label(root, text="and Paxton Wills", fg="blue", cursor="hand2")
        link1.grid(row=40, column=1, columnspan=1, sticky="w")
        link1.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/PaxAmericana"))

    # Start Button Action
    def call_program(self):

        # Message
        self.message.config(text="APPLICATION IS RUNNING", bg="green")

        # Prompt user for file path
        self.file_path = tk_dialog.asksaveasfilename(defaultextension=".py")
        if not self.file_path:
            self.message.config(text="NO FILE WAS CHOSEN", bg="#f04a4a")
            return

        # Button map
        self.button_map = self.get_button_map()

        # Run program, data will be added to self.recorded_data
        self.start_listener()

        # Save recorded_data to a file. This is handled in format2pyautogui.py
        write_output_file(recorded_data=self.recorded_data, save_file_path=self.file_path)

        # Message
        self.message.config(text="APPLICATION STOPPED, DATA IS SAVED", bg="#3281a8")

        # Bring window to the front
        root.attributes('-topmost', 1)
        root.attributes('-topmost', 0)

    # Get a dictionary of key mapping
    def get_button_map(self) -> dict:
        # Map Options to Keys
        option_map = {
            "Scroll Lock": Key.scroll_lock,
            "Num Lock": Key.num_lock,
            "Caps Lock": Key.caps_lock,
            "None": "None",
        }
        # Map var_name to chosen button from main GUI
        button_map = {
            "recording": self.recording_trigger_key.get(),
            "img_capturing": self.img_trigger_key.get(),
        }
        # Map var_name to Keys
        for key, val in button_map.items():
            button_map[key] = option_map[str(val)]
        return button_map

    # Main program, this is the recorder
    def start_listener(self) -> None:
        # Controller
        mouse = MouseController()
        keyboard = KeyboardController()

        # Set up variable
        save_dir = self.file_path.rsplit("/", 1)[0]
        mouse_top_left_corner = ()
        count = 0
        recording = img_capturing = False
        # These keys won't be recorded
        functional_keys = list(self.button_map.values()) + [Key.esc]

        # Mkdir /images to store images
        def make_image_dir(path):
            try:
                os.mkdir(path + "/images")
            except FileExistsError:
                pass

        # Key pressed event
        def on_press(key):
            nonlocal mouse_top_left_corner, count, recording, img_capturing

            # Start Image Capturing
            if key == self.button_map["img_capturing"]:
                print("Start Image Capturing" if not img_capturing else "Stop Image Capturing")
                img_capturing = not img_capturing
                make_image_dir(save_dir)

            # Record Image top-left pos
            if key == Key.shift and img_capturing:
                print(f"Top left image location: {mouse.position}")
                mouse_top_left_corner = mouse.position

            # Record Image bot-right pos
            if key == Key.ctrl_l and mouse_top_left_corner and img_capturing:
                print(f"Image captured from {mouse_top_left_corner} to "
                      f"{mouse.position} is save as screen_shot_{count}.png")
                end = [mouse.position[i] - mouse_top_left_corner[i] for i in range(2)]
                save_image_name = f'screen_shot_{count}'
                save_image_path = f"{save_dir}/images/{save_image_name}.png"
                pyautogui.screenshot(region=(*mouse_top_left_corner, *end)).save(save_image_path)
                self.recorded_data.append(img2pyautogui(f"{save_dir}/images/", save_image_name))
                mouse_top_left_corner = ()
                count += 1

            # Start Recording
            if key == self.button_map["recording"]:
                print("Start Recording" if not recording else "Stop Recording")
                recording = not recording

            # Stop Listener
            if key == Key.esc:
                print("Stop program")
                return False

            # Record other keys
            elif recording and (not img_capturing) and (key not in functional_keys):
                self.recorded_data.append(keyboard2pyautogui(key_pressed=key))
                print(keyboard2pyautogui(key_pressed=key))

        # Key released event
        def on_release(key):
            pass

        # Mouse moved event
        def on_move(x, y):
            pass

        # Mouse clicked event
        def on_click(x, y, button, pressed):
            if pressed and recording and (not img_capturing):
                self.recorded_data.append(mouse2pyautogui(x=x, y=y, button=button))
                print(mouse2pyautogui(x=x, y=y, button=button))

        # Mouse scrolled event
        def on_scroll(x, y, dx, dy):
            if recording and (not img_capturing):
                self.recorded_data.append(mouse2pyautogui(x=x, y=y, dx=dx, dy=dy))
                print(mouse2pyautogui(x=x, y=y, dx=dx, dy=dy))

        # Start listening
        with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll):
            with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
                listener.join()


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)  # .pack(side="top", fill="both")
    root.mainloop()
