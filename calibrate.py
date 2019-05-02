import pygame, sys, time, random
from pygame.locals import *

import cv2
from gaze_tracking import GazeTracking

currentPosition = [500, 368]


def move_left():
    currentPosition[0] -= 20


def move_right():
    currentPosition[0] += 20


def move_up():
    currentPosition[1] -= 20
    currentPosition[0] -= 40


def move_down():
    currentPosition[1] += 20


def find_average(coordinates):
    coordinate_sum = 0
    for point in coordinates:
        coordinate_sum += point
    return coordinate_sum / len(coordinates)


pygame.init()

windowCalibration = pygame.display.set_mode((0, 0), FULLSCREEN)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

f = open("calibration_settings.txt", "w+")

state = "center"
time_delay = 3000
wait_to = 0

windowCalibration.fill(WHITE)

pygame.display.set_caption("Eye calibration")
pygame.draw.circle(windowCalibration, (0, 0, 0), currentPosition, 10)

done = False
successful = False
clock = pygame.time.Clock()

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

#Store the values for calibration

minXCoordinates = []
minYCoordinates = []
maxXCoordinates = []
maxYCoordinates = []
centerCoordinates = []
minimumXCoordinate = 0
maximumXCoordinate = 0
minimumYCoordinate = 0
maximumYCoordinate = 0
ycoordinates = []
currentXCoordinate = 0
currentYCoordinate = 0
while not done:
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

    if state == "center":
    elif state == "right":
    elif state == "left":
    elif state == "up":
    elif state == "down":

    windowCalibration.fill(WHITE)
    pygame.draw.circle(windowCalibration, BLACK, currentPosition, 10)
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
if successful:
    f.write(str(minimumXCoordinate) + "\n")
    f.write(str(maximumXCoordinate) + "\n")
    f.write(str(minimumYCoordinate) + "\n")
    f.write(str(maximumYCoordinate) + "\n")
    print("Minimum X is " + str(minimumXCoordinate))
    print("Maximum X is " + str(maximumXCoordinate))
    print("Minimum Y is " + str(minimumYCoordinate))
    print("Maximum Y is " + str(maximumYCoordinate))
f.close()
