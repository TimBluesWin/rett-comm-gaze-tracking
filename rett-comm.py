"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import ctypes
import statistics
import webbrowser
import numpy as np
import random

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


# Not every frame, calculate only every 5 frames.

frame_count = 0
webbrowser.open("http://localhost/rett-comm-web-application/indonesian/mainMenu.php")
cv2.namedWindow("Demo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Demo", (100, 100))
cv2.moveWindow("Demo", int(gaze.screenWidth / 2) - 100, int(gaze.screenHeight) - 220)
left_border = gaze.border
right_border = gaze.screenWidth - left_border
center_y = int(gaze.screenHeight / 2)
while True:
    # We will use deque to store the x value every 5 frames.
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    if gaze.pupils_located:
        current_x = gaze.get_x_coordinate()
        if current_x < left_border:
            randomised_x_coordinate = random.randint(left_border, left_border + 10)
            ctypes.windll.user32.SetCursorPos(randomised_x_coordinate, center_y)
        elif current_x > right_border:
            randomised_x_coordinate = random.randint(right_border - 10, right_border)
            ctypes.windll.user32.SetCursorPos(randomised_x_coordinate, center_y)
        else:
            ctypes.windll.user32.SetCursorPos(int(current_x), int(0.5 * 768))
    if cv2.waitKey(1) == 27:
        break
