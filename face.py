#"Rayo emprendedor" filter 
#Based on Instagram Face Filter
#Original by Sergio Canu on https://pysource.com/2019/03/25/pigs-nose-instagram-face-filter-opencv-with-python/
#Face landmark map by Sergio Canu
#Modified by Manuel Cota

import cv2 as cv
import numpy as np
import dlib
from math import hypot

def face_tracker():
    #Loading Camera and Nose image and Creating mask
    cap = cv.VideoCapture(0)
    l_image = cv.imread("lightning_emoji.png")
    _, frame = cap.read()
    rens = frame.shape[1]
    cols = frame.shape[0]
    nose_mask = np.zeros((rens,cols), np.uint8)

    #Loading Face Detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    while True:
        _, frame = cap.read()
        nose_mask.fill(0)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = detector(frame)
        
        for face in faces:
            landmarks = predictor(gray_frame, face)

            #Nose coordinates
            top_nose = (landmarks.part(29).x, landmarks.part(29).y)
            center_nose = (landmarks.part(30).x, landmarks.part(30).y)
            left_nose = (landmarks.part(31).x, landmarks.part(31).y)
            right_nose = (landmarks.part(35).x, landmarks.part(35).y)

            nose_width = int(hypot(left_nose[0] - right_nose[0],left_nose[1] - right_nose[1]) * 1.7)

            nose_height = int(nose_width * 1.5)

            #New nose position
            top_left = (int (center_nose[0] - nose_width / 2), int(center_nose[1] - nose_height / 2))

            bottom_right = (int(center_nose[0] + nose_width / 2), int(center_nose[1] + nose_height / 2))

            #Adding new nose
            nose_light = cv.resize(l_image, (nose_width, nose_height))
            nose_light_gray = cv.cvtColor(nose_light, cv.COLOR_BGR2GRAY)
            _, nose_mask = cv.threshold(nose_light_gray, 25, 255, cv.THRESH_BINARY_INV)
            nose_area = frame[top_left[1]: top_left[1] + nose_height,top_left[0]: top_left[0] + nose_width]

            nose_area_no_nose = frame[top_left[1]: top_left[1] + nose_height, top_left[0]: top_left[0] + nose_width]

            final_nose = cv.add(nose_area_no_nose, nose_light)
            frame[top_left[1]: top_left[1] + nose_height,top_left[0]: top_left[0] + nose_width] = final_nose

            #cv.imshow("Nose area", nose_area)
            #cv.imshow("Nose pig", nose_light)
            #cv.imshow("final nose", final_nose)
            cv.imshow("Frame", frame)
            
        key = cv.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv.destroyAllWindows()

face_tracker()