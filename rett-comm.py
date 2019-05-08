"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import os
import ctypes
from collections import deque
import statistics
import webbrowser

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)


#Not every frame, calculate only every 5 frames.

frame_count = 0
x_coordinates = deque([], 3)
webbrowser.open("http://localhost/rett-comm/program/mainMenu2.html")
while True:
    #We will use deque to store the x value every 5 frames.
    frame_count = (frame_count + 1) % 3
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
    #height = gaze.get_eye_height_left()
    #print "y displacement from eye corner is " + str(height)
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    
    if gaze.pupils_located:
        #cv2.imshow("Eye", gaze.eye_left.frame)
        print "Width is " + str(gaze.get_eye_width_left())
        print "Center is " + str(gaze.get_eye_center_left())
        print "Displacement is " + str(gaze.get_x_displacement_left())
        x_coordinates.append(int(gaze.get_x_coordinate()))
        if frame_count % 3 == 0:
            median_x_coordinate = statistics.median(x_coordinates)
            ctypes.windll.user32.SetCursorPos(int(median_x_coordinate), int(0.5 * 768))
		
        #os.system("xdotool mousemove " + str(int(gaze.get_x_coordinate())) + " " + str(gaze.vertical_ratio() * 768))
    #timmy
    #if gaze.pupils_located:
    #    os.system("xdotool mousemove " + str((1-gaze.horizontal_ratio()) * 1377) + " " + str(368))
    #end timmy
	
	
	
    if cv2.waitKey(1) == 27:
        break
