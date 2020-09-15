import numpy
import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import os

parser = argparse.ArgumentParser(description = 'Image Convolution')
parser.add_argument('-f','--file',default="", help="Introduce file name.")
args = vars(parser.parse_args())

if args["file"] == "":
    print("Enter the file name (default: sample.png): ",end="")
    args["file"] = input()
    if args["file"] == "":
        args["file"] = "sample.png"

image = cv.imread(args["file"])
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

kernelx = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
kernely = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)
kernelxy = numpy.array(([2,4,2],[4,8,4],[2,4,2]),numpy.float32)
kernel = numpy.array(([-2,-2,0],[-2,0,2],[0,2,2]),numpy.float32)

outputx = cv.filter2D(image, -1, kernelx)
outputy = cv.filter2D(image, -1, kernely)
outputxy = cv.filter2D(image, -1, kernelxy)
outputxpy = cv.filter2D(image,-1,kernel)
output = cv.add(outputx,outputy)


if not os.path.exists('out'):
    os.makedirs('out')

cv.imwrite("out/"+args["file"]+"x.png", outputx)
cv.imwrite("out/"+args["file"]+"y.png", outputy)
cv.imwrite("out/"+args["file"]+"xy.png", outputxy)
cv.imwrite("out/"+args["file"]+"xpy.png", outputxpy)
cv.imwrite("out/"+args["file"]+".png", output)
