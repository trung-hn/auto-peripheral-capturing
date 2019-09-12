Things to consider:
- Using "Alt" as the capture key. 
  - By holding down "Alt" action performed during that time is recorded
  - Alt is chosen by default. User can select another key
    - Capture key should not record itself
- Apply image recognition for button that moves around
  - Decide the range of searching. 
- Make a GUI using PyQt5


Pax notes 9/12/2019
-when you want to expand a window to fullscreen, the top right expand button is not a great option because:
1. difficult to capture as an image due to top/left to bottom/right method of imagecapturing and 
2. it's often not a unique image because that button is the same for most windows
Therefore, it may be best to select an image of the top left and use double click
### i implemented a feature so that the mouse will double click if the image name contains 'expand'
- you can use the backtick ` to denote that you are typing a comment into the code during recording

Future features
-recognizing shift before a key, and then processing it as hotkey(['shift'],'a')
