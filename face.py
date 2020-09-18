#"Rayo emprendedor" filter 
#Based on Instagram Face Filter
#Original by Sergio Canu on https://pysource.com/2019/03/25/pigs-nose-instagram-face-filter-opencv-with-python/
#Face landmark map by Sergio Canu
#Modified by Manuel Cota
import cv2 as cv
from math import hypot

def face_tracker(frame, l_image,rens,cols,face_mask, detector, predictor, gray_frame, faces):
    cont = 0
    for face in faces:
        cont+=1
    if cont < 1:
        return frame
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
        return frame