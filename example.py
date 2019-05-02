"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import os

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    #if gaze.is_blinking():
    #    text = "Blinking"
    if gaze.is_right():
        text = "Looking right"
        
        #print "right"
    elif gaze.is_left():
        text = "Looking left"
        
        #print "left"
    #elif gaze.is_center():
    #    text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    
    if gaze.pupils_located:
        cv2.imshow("Eye", gaze.eye_left.frame)
        os.system("xdotool mousemove " + str(int(gaze.get_x_coordinate())) + " " + str(368))
    #timmy
    #if gaze.pupils_located:
    #    os.system("xdotool mousemove " + str((1-gaze.horizontal_ratio()) * 1377) + " " + str(368))
    #end timmy
    if cv2.waitKey(1) == 27:
        break
