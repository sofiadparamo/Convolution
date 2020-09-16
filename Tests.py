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
#kernel = numpy.array(([0,0,0],[0,1,0],[0,0,0]),numpy.float32)

image_row, image_col, image_chan = image.shape
kernelX_row, kernelX_col = kernelX.shape
kernelY_row, kernelY_col = kernelY.shape

outputX = numpy.zeros(image.shape)
outputY = numpy.zeros(image.shape)

for row in range(image_row):
    for col in range(image_col):
        outputX[row,col,0] = conv_helper(image[row-1:row + 1, col-1:col + 1,0], kernelX)
        outputX[row,col,1] = conv_helper(image[row-1:row + 1, col-1:col + 1,1], kernelX)
        outputX[row,col,2] = conv_helper(image[row-1:row + 1, col-1:col + 1,2], kernelX)

for row in range(image_row):
    for col in range(image_col):
        outputY[row,col,0] = conv_helper(image[row-1:row + 1, col-1:col + 1,0], kernelY)
        outputY[row,col,1] = conv_helper(image[row-1:row + 1, col-1:col + 1,1], kernelY)
        outputY[row,col,2] = conv_helper(image[row-1:row + 1, col-1:col + 1,2], kernelY)

output = cv.add(outputX,outputY)

while(True):
    cv.imshow('frame', output)
    k = cv.waitKey(10)
    if k == 27:
        break
