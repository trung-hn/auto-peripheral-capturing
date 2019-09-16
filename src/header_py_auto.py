# This file contains GUI automation code
# run using a python 3 interpreter

from pyautogui import *
from time import sleep


# finds and then selects the image
def select(image):
    location = find(image)
    if 'expand' in image:
        doubleClick(location, duration=.25)
    else:
        click(location, duration=.25)
    sleep(1)
    return None


# finds location, continues looking until it finds the image
def find(image):
    while True:
        try:
            # changing the confidence can help you locate images
            location = locateOnScreen(image, confidence=.9)
            return location
        except:
            print('Searching for : ' + image)


def start_mod_file_builder():
    # open a new tab with MoD
    hotkey('winleft', 'r', duration=.25)
    sleep(.25)
    Mod_filebuilder_path = r'C:\Program Files (x86)\PTI\PSSMODFileBuilder\MODFileBuilder.exe'
    typewrite(Mod_filebuilder_path)
    typewrite(['enter'])


start_mod_file_builder()
sleep(5)

#### end of header ###
