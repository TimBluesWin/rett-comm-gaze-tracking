from __future__ import division
import pyautogui
import pylint
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration


class GazeTracking(object):


    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()
        self.screenWidth = pyautogui.size()[0]
        self.screenHeight = pyautogui.size()[1]
    
        self.border = 60

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None
        except cv2.error as e:
            self.eye_left = None
            self.eye_right = None
            print("Terjadi kesalahan dalam pemrosesan muka \n" + sys.exec_info[2])

    def refresh(self, frame):
        """Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def leftmost_screen(self):
        return self.border

    def rightmost_screen(self):
        return self.screenWidth - self.border
    
    def get_option_area_with_border(self):
        return (self.rightmost_screen() - self.leftmost_screen()) / 2

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_left.pupil.x
            y = self.eye_right.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        horizontal direction of the gaze. The extreme right is 0.0,
        the center is 0.5 and the extreme left is 1.0
        """
        if self.pupils_located:
            
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 that indicates the
        vertical direction of the gaze. The extreme top is 0.0,
        the center is 0.5 and the extreme bottom is 1.0
        """
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2
    
    def get_horizontal_ratio_from_eye_corners(self):
        width = self.get_eye_width_left()
        displacement = self.get_x_displacement_left()
        return displacement / width
    
    #TODO: Implement vertical ratio.

    def get_vertical_ratio_from_eye_corners(self):
        return None

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.45

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.55

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8
   
    def get_eye_center_left(self):
    #this time we use eye corners as a reference to the eye center.
        if self.pupils_located:
            left_eye_left_corner, left_eye_right_corner = (self.eye_left.left_corner, self.eye_left.right_corner)
            return ((left_eye_left_corner[0] + left_eye_right_corner[0])/2, (left_eye_left_corner[1] + left_eye_right_corner[1]) / 2)

    def get_eye_center_right(self):
        if self.pupils_located:
            right_eye_left_corner, right_eye_right_corner = (self.eye_right.left_corner, self.eye_right.right_corner)
            return ((right_eye_left_corner[0] + right_eye_right_corner[0])/2, (right_eye_left_corner[1] + right_eye_right_corner[1]) / 2)
    
    def get_eye_width_left(self):
        if self.pupils_located:
            return self.eye_left.right_corner[0] - self.eye_left.left_corner[0]

    def get_eye_width_right(self):
        if self.pupils_located:
            return self.eye_right.right_corner[0] - self.eye_right.left_corner[0]

    def get_y_displacement_left(self):
        #Best way I think is d
        if self.pupils_located:
            displacement = self.pupil_left_coords()[1] - self.eye_left.left_corner[1]
            return displacement

    def get_y_displacement_right(self):
        if self.pupils_located:
            displacement = self.pupil_right_coords()[1] - self.eye_right.left_corner[1]
            return displacement
    
    def get_left_eye_left_corner(self):
        if self.pupils_located:
            return self.eye_left.left_corner

    def get_right_eye_left_corner(self):
        if self.pupils_located:
            return self.eye_right.right_corner

    def get_x_displacement_left(self):
        if self.pupils_located:
            displacement_left = self.pupil_left_coords()[0] - self.eye_left.left_corner[0]
            
            return displacement_left
    def get_x_displacement_right(self):
        if self.pupils_located:
            
            displacement_right = self.pupil_right_coords()[0] - self.eye_right.left_corner[0]
            return displacement_right
    def get_vertical_position(self):
        if self.pupils_located:
            displacement_left = None
            displacement_right = None

    #We need to sesuaikan rationya, to accomodate different viewing distance.

    def get_x_coordinate(self):
        if self.pupils_located:
            calibrationExists = os.path.isfile("calibration_settings.txt")
            if calibrationExists:
                f = open("calibration_settings.txt", "r")
                data = f.readlines()
                #First line: Pas ngeliat center
                #Second line: Pas liat kanan
                #Third line: Pas liat kiri
				#We need to modify the thresholds according to how far our eyes
                #calibratedEyeWidth = data[3]
                #actualEyeWidth = self.get_eye_width_left()
                #adjustment_ratio = actualEyeWidth / float(calibratedEyeWidth)
                centerX = float(data[0])
                minX = float(data[1])
                maxX = float(data[2])
                #centerX = float(data[0]) 
                #minX = float(data[1])
                #maxX = float(data[2])
                ratio = self.get_horizontal_ratio_from_eye_corners()
                #print "Displacement of X Coordinate is " + str(displacement)
                if ratio > maxX:
                    ratio = maxX
                elif ratio < minX:
                    ratio = minX
                if ratio <= centerX:
                    #That means we see right, thanks to the inversion at webcam
                    try:
                        #return 1366 - ((displacement - minX) / (centerX - minX)) * 688
                        return self.rightmost_screen()- ((ratio - minX) / (centerX - minX)) * 1.1 * self.get_option_area_with_border()
                    except ZeroDivisionError:
					    #If division by zero then failsafenya return paling tengah
                        return self.screenWidth / 2
                else:
                    try:
                        #return ((maxX - displacement) / (maxX - centerX)) * 688
                        return self.leftmost_screen() + ((maxX - ratio) / (maxX - centerX)) * 1.1 * self.get_option_area_with_border()
                    except ZeroDivisionError:
                        return self.screenWidth / 2
               
            else:  
            #Take the region between the left corner and right corner, measure how much the displacement between center, and calculate the displacement against the 
                displacement_left = self.pupil_left_coords()[0] - self.eye_left.left_corner[0]
                #print("Displacement left is " + str(displacement_left))
                displacement_right = self.pupil_right_coords()[0] - self.eye_right.left_corner[0]
                #print("Displacement Right is " + str(displacement_right))
                #print("Eye Width is " + str(self.get_eye_width_left()))
            #print "X coordinate is " + str(((1- displacement_left / self.get_eye_width_left()) + (1-displacement_right / self.get_eye_width_right())) / 2 * 1366)
                ratio_left = 1 - (displacement_left / self.get_eye_width_left())
            #ratio_right = 1 - (displacement_right / self.get_eye_width_right())
                return ratio_left * 1366

    def get_y_coordinate(self):
        return None

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            #timmy
            left_eye_left_corner, left_eye_right_corner = (self.eye_left.left_corner, self.eye_left.right_corner) 
            right_eye_left_corner, right_eye_right_corner = (self.eye_right.left_corner, self.eye_right.right_corner)
            left_eye_top, left_eye_bottom = (self.eye_left.eye_upper, self.eye_left.eye_lower)
            right_eye_top, right_eye_bottom = (self.eye_right.eye_upper, self.eye_right.eye_lower)
            left_eye_center = ((left_eye_left_corner[0] + left_eye_right_corner[0])/2, (left_eye_left_corner[1] + left_eye_right_corner[1]) / 2)
            right_eye_center = ((right_eye_left_corner[0] + right_eye_right_corner[0])/2, (right_eye_left_corner[1] + right_eye_right_corner[1]) / 2)
            #right_eye_left_corner, right_eye_right_corner = None
            
            cv2.circle(frame, (left_eye_left_corner[0], left_eye_left_corner[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (left_eye_right_corner[0], left_eye_right_corner[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (left_eye_top[0], left_eye_top[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (left_eye_bottom[0], left_eye_bottom[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (int(left_eye_center[0]), int(left_eye_center[1])), 5, (0, 0, 255), -1)
            cv2.circle(frame, (right_eye_left_corner[0], right_eye_left_corner[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (right_eye_right_corner[0], right_eye_right_corner[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (right_eye_top[0], right_eye_top[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (right_eye_bottom[0], right_eye_bottom[1]), 3, (0, 0, 255), -1)
            cv2.circle(frame, (int(right_eye_center[0]), int(right_eye_center[1])), 5, (0, 0, 255), -1)
            cv2.line(frame, (left_eye_left_corner[0], left_eye_left_corner[1]), (x_left, y_left), color)
            cv2.line(frame, (left_eye_right_corner[0], left_eye_right_corner[1]), (x_left, y_left), color)
            #end timmy
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)
        return frame
