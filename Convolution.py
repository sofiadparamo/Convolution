#Hola

import numpy
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import os
import time

parser = argparse.ArgumentParser(description = 'Image Convolution')
parser.add_argument('-f','--file',default="", help="Introduce file name.")
parser.add_argument('-i','--cameraSource',default=0, help="Introduce number or camera pathm default is 0 (default cam)")
args = vars(parser.parse_args())

if args["file"] != "":
    image = cv.imread(args["file"])
    #image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    kernelx = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
    kernely = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)
    #kernel = numpy.array(([0,0,0],[0,1,0],[0,0,0]),numpy.float32)
    
    outputx = cv.filter2D(image, -1, kernelx)
    outputy = cv.filter2D(image, -1, kernely)
    output = cv.add(outputx,outputy)
    #output = cv.filter2D(image, -1, kernel)

    if not os.path.exists('out'):
        os.makedirs('out')
    cv.imwrite("out/"+args["file"][:-4]+".png", output)
else: 
    script_start_time = time.time()

    vid = cv.VideoCapture(int(args["cameraSource"])) 
      
    while(vid.isOpened()): 
        success, frame = vid.read() 
        
        if not success:
            continue
        if frame is None:
            continue
            
        frame = cv.medianBlur(frame,5)
        
        kernelx = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
        kernely = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)
        
        
        outputx = cv.filter2D(frame, -1, kernelx)
        outputy = cv.filter2D(frame, -1, kernely)
        output = cv.add(outputx,outputy)
      
        cv.imshow('frame', output) 
          
        k = cv.waitKey(10)
        if k == 27:
            break
    
    vid.release() 
    cv.destroyAllWindows() 
    
    
    print('Script took %f seconds.' % (time.time() - script_start_time))
