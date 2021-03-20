# This file contains GUI automation code
# run using a python 3 interpreter

import pyautogui
from time import sleep


# finds and then selects the image
def find_and_click_image(image):
    location = find(image)
    if 'expand' in image:
        pyautogui.doubleClick(location, duration=.25)
    else:
        pyautogui.click(location, duration=.25)
    sleep(1)
    return None


# finds location, continues looking until it finds the image
def find(image):
    while True:
        try:
            # changing the confidence can help you locate images
            location = pyautogui.locateOnScreen(image, confidence=.9)
            return location
        except:
            print('Searching for : ' + image)


set_duration = 1
# start_mod_file_builder()
sleep(3)
#### end of header ###
