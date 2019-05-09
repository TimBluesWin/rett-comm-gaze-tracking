import pygame, sys, time, random
from pygame.locals import *

import cv2
from gaze_tracking import GazeTracking

import statistics
import pyautogui

from tkinter import messagebox

pygame.init()

pygame.mixer.music.load("ding.wav")

windowCalibration = pygame.display.set_mode((0, 0), FULLSCREEN)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

f = open("calibration_settings.txt", "w+")

state = "center"
time_delay = 3000
wait_to = 0

windowCalibration.fill(WHITE)

pygame.display.set_caption("Eye calibration")
done = False
successful = False
clock = pygame.time.Clock()

gaze = GazeTracking()

screen_width = pyautogui.size()[0]
screen_height = pyautogui.size()[1]
center_x = int(screen_width / 2)
center_y = int(screen_height / 2)
from_edge = 60

currentPosition = [center_x, center_y]

webcam = cv2.VideoCapture(0)

#Store the values for calibration

#eyeWidths = []

leftXCoordinates = []
leftYCoordinates = []
rightXCoordinates = []
rightYCoordinates = []
xCoordinate = 0
yCoordinate = 0
wait_to = pygame.time.get_ticks() + 3000
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            successful = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                successful = False
    _, frame = webcam.read()
    gaze.refresh(frame)
    #Clear all elements after changing state by using list.clear
    #eyeWidths.append(gaze.get_eye_width_left())
    if state == "center":
        current_time = pygame.time.get_ticks()
        if gaze.pupils_located:
            leftXCoordinates.append(gaze.get_horizontal_ratio_from_eye_corners())
            print (gaze.get_horizontal_ratio_from_eye_corners())
            #leftXCoordinates.append(gaze.get_x_displacement_left())
            #rightXCoordinates.append(gaze.get_x_displacement_right())
        #centerXCoordinates.append()
        #centerYCoordinates.append()
        if current_time > wait_to:
            #print "Going to right"
            if not leftXCoordinates:
                done = True
                successful = False
            else:
                xCoordinate = (statistics.median(leftXCoordinates))
                f.write(str(xCoordinate) + "\n")
                leftXCoordinates = []
                currentPosition = [screen_width - from_edge, int(screen_height / 2)]
                wait_to = pygame.time.get_ticks() + 3000
                state = "right"
                pygame.mixer.music.play()
            
    #elif state == "middle_right":
    #    current_time = pygame.time.get_ticks()
    #    if current_time > wait_to:
    #        #print "Going to right"
    #        currentPosition = [1300, 368]
    #        wait_to = pygame.time.get_ticks() + 3000
    #        state = "right"
    elif state == "right":
        current_time = pygame.time.get_ticks()
        if gaze.pupils_located:
            leftXCoordinates.append(gaze.get_horizontal_ratio_from_eye_corners())
            #rightXCoordinates.append(gaze.get_x_displacement_right())
        if current_time > wait_to:
            if not leftXCoordinates:
                done = True
                successful = False
            else:
                xCoordinate = (statistics.median(leftXCoordinates))
                f.write(str(xCoordinate) + "\n")
                leftXCoordinates = []
            #rightXCoordinates = []
                currentPosition = [from_edge, int(screen_height / 2)]
                pygame.mixer.music.play()
                wait_to = pygame.time.get_ticks() + 3000
                state = "left"
    #elif state == "middle_left":
    #    current_time = pygame.time.get_ticks()
    #    if current_time > wait_to:
    #        currentPosition = [50, 368]
    #        wait_to = pygame.time.get_ticks() + 3000
    #        state = "middle_left"
    elif state == "left":
        current_time = pygame.time.get_ticks()
        if gaze.pupils_located:
            leftXCoordinates.append(gaze.get_horizontal_ratio_from_eye_corners())
        if current_time > wait_to:
            if not leftXCoordinates:
                done = True
                successful = False
            else:
                xCoordinate = (statistics.median(leftXCoordinates))
                f.write(str(xCoordinate) + "\n")
                leftXCoordinates = []
                pygame.mixer.music.play()
            #currentPosition = [677, 700]
            #wait_to = pygame.time.get_ticks() + 3000
            #state = "down"
            
            #myEyeWidth = statistics.median(eyeWidths)
            #f.write(str(myEyeWidth) + "\n")
                done = True
                successful = True
    #elif state == "down":
    #    current_time = pygame.time.get_ticks()
    #    if current_time > wait_to:
    #        currentPosition = [677, 50]
    #        wait_to = pygame.time.get_ticks() + 3000
    #        state = "up"
    #elif state == "up":
    #    current_time = pygame.time.get_ticks()
    #    if current_time > wait_to:
    #        done = True

    windowCalibration.fill(WHITE)
    pygame.draw.circle(windowCalibration, GREEN, currentPosition , 10)
    pygame.display.update()



# First: Create background (done)
# Second: Create circle (nanti bisa diganti ama gambar Masha). This will be used for the eye to follow. (done)
# Third: Make the circle move dlu aja.
# 3a: Circle move to the desired position Pertama to the extreme left, kedua to the extreme right, ketiga to the exteme
# top, keempat to the extreme bottom
# Fourth:
"""
Extreme left: Leftmost X coordinate
Extreme Right: Rightmost X coordinate
Extreme top: Topmost Y Coordinate
Extreme Bottom: Bottom most Y coordinate.
From the example program, we create this object, then....
"""
# Fifth: Activate Webcam, and incorporate the eye tracker to get the eye positions
# Maybe we need to have an array, and average the results of the extreme coordinates.
# Example incorporating python library can take variable from here.
# Possible to store the values on a file instead; nanti kalau ketemu algoritma lain bisa langsung pake.
f.close()
if not successful:
    messagebox.showinfo("Kalibrasi Gagal", "Kalibrasi Gagal. Mata kamu tidak terdeteksi.")