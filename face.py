#"Rayo emprendedor" filter 
#Based on Instagram Face Filter
#Original by Sergio Canu on https://pysource.com/2019/03/25/pigs-nose-instagram-face-filter-opencv-with-python/
#Face landmark map by Sergio Canu
#Modified by Manuel Cota

import cv2 as cv
import numpy
import dlib
from math import hypot

def face_tracker():
    #Loading Camera and Nose image and Creating mask
    cap = cv.VideoCapture(0)
    l_image = cv.imread("lightning_emoji.png")
    _, frame = cap.read()
    rens = frame.shape[1]
    cols = frame.shape[0]
    face_mask = numpy.zeros((rens,cols), numpy.uint8)

    #Loading Face Detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    while True:
        _, frame = cap.read()
        face_mask.fill(0)
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        faces = detector(frame)
        
        for face in faces:
            landmarks = predictor(gray_frame, face)

            #Face coords
            top_face = (landmarks.part(21).x + 1000, 
                        landmarks.part(27).y + 1000)

            center_face = (landmarks.part(27).x, 
                           landmarks.part(27).y)

            left_face = (landmarks.part(21).x, 
                         landmarks.part(21).y)

            right_face = (landmarks.part(22).x, 
                          landmarks.part(22).y)

            face_width = int(hypot(left_face[0] - 
                             right_face[0],
                             left_face[1] - 
                             right_face[1]) * 1.77)

            face_height = int(face_width * 2.2)

            #New face position
            top_left = (int (center_face[0] - face_width / 2), 
                        int(center_face[1] - face_height / 2))

            bottom_right = (int(center_face[0] + face_width / 2), 
                            int(center_face[1] + face_height / 2))

            #Adding new face
            face_light = cv.resize(l_image, (face_width, face_height))

            face_light_gray = cv.cvtColor(face_light, cv.COLOR_BGR2GRAY)
            _, face_mask = cv.threshold(face_light_gray, 
                                        25, 
                                        255, 
                                        cv.THRESH_BINARY_INV)

            face_area = frame[top_left[1]: top_left[1] + 
                              face_height,top_left[0]: top_left[0] + 
                              face_width]

            face_area_no_face = frame[top_left[1]: top_left[1] + 
                                      face_height, top_left[0]: top_left[0] +
                                      face_width]

            final_face = cv.add(face_area_no_face, face_light)
            frame[top_left[1]: top_left[1] + 
            face_height,top_left[0]: top_left[0] + 
            face_width] = final_face

            #Render windows, for functionality demo purposes
            #cv.imshow("Face area", face_area)
            #cv.imshow("Face pig", face_light)
            #cv.imshow("final face", final_face)

            #Final product
            cv.imshow("Frame", frame)
        
        #Close windows
        key = cv.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv.destroyAllWindows()

face_tracker()