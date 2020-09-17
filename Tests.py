import numpy
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import os
import time

def conv_helper(fragment, kernel):
    """ multiplica 2 matices y devuelve su suma"""
    
    f_row, f_col = fragment.shape
    k_row, k_col = kernel.shape 
    result = 0.0
    for row in range(f_row):
        for col in range(f_col):
            #print(fragment[row,col],kernel[row,col])
            result += fragment[row,col] *  kernel[row,col]
    #print("Result:",result)
    return result

image = cv.imread("sample.jpg")

kernelX = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
kernelY = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)
# kernel = numpy.array(([0,0,0],[0,1,0],[0,0,0]),numpy.float32)

image_row, image_col, image_chan = image.shape
kernelX_row, kernelX_col = kernelX.shape
kernelY_row, kernelY_col = kernelY.shape

outputX = numpy.zeros((image_row,image_col))
outputY = numpy.zeros((image_row,image_col))

print(image_row)

for row in range(image_row-1):
    for col in range(image_col-1):
        outputX[row+1,col+1] = conv_helper(image[row:row + kernelX_row, col:col + kernelX_col,0], kernelX)

for row in range(image_row-1):
    for col in range(image_col-1):
        outputY[row+1,col+1] = conv_helper(image[row:row + kernelY_row, col:col + kernelY_col,0], kernelY)
        

output = cv.add(outputX,outputY)

while(True):
    cv.imshow('frame', output)
    k = cv.waitKey(10)
    if k == 27:
        break
