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
    variant = 0
    blur = False
    script_start_time = time.time()
    
    vid = cv.VideoCapture(int(args["cameraSource"])) 
      
    while(vid.isOpened()): 
        success, frame = vid.read() 
        
        if not success:
            continue
        if frame is None:
            continue
        
        if(blur):
            frame = cv.medianBlur(frame,5) # Apply an median blur effect for noise reduction
        print(blur)
        
        
        if(variant%3 == 0):
            kernel = numpy.array(([0,0,0],[0,1,0],[0,0,0]),numpy.float32)
            output = cv.filter2D(frame, -1, kernel)
        elif(variant%3 == 1):
            kernelx = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
            kernely = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)
            outputx = cv.filter2D(frame, -1, kernelx)
            outputy = cv.filter2D(frame, -1, kernely)
            output = cv.add(outputx,outputy)
        elif(variant%3 == 2):
            kernel = numpy.array(([0,1,0],[1,1,1],[0,1,0]),numpy.float32)
            output = cv.filter2D(frame, -1, kernel)
      
        cv.imshow('frame', output) 
        
        k = cv.waitKey(10)
        if k == 27: # Cuando se pulsa esc.
            break
        elif k == 98: # Cuando se pulsa espacio
            if blur:
                blur = False
            else:
                blur = True
        elif k == 32: # Cuando se pulsa "b"
            variant+=1
            
    
    vid.release() 
    cv.destroyAllWindows() 
    
    
    print('Script took %f seconds.' % (time.time() - script_start_time))
