import numpy 
import argparse
import os
import time
import dlib
import cv2 as cv
from math import hypot
from face import face_tracker

# Descripción para argumentos del script
parser = argparse.ArgumentParser(description = 'Image Convolution')
parser.add_argument('-f','--file', default="", help="Introduce file name.")
parser.add_argument('-i','--cameraSource', default=0, help="Introduce number or camera pathm default is 0 (default cam)")
args = vars(parser.parse_args())

if args["file"] != "": # Si el argumento "file" no está en blanco
    image = cv.imread(args["file"])

    # Kernel por aplicar
    kernelx = numpy.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]), numpy.float32)
    kernely = numpy.array(([-1, -2, -1], [0, 0, 0], [1, 2, 1]), numpy.float32)
    
    # Kernel aplicado a la convolucion
    outputx = cv.filter2D(image, -1, kernelx)
    outputy = cv.filter2D(image, -1, kernely)
    
    output = cv.add(outputx, outputy) # Suma aritmetica de las dos imagenes

    if not os.path.exists('out'): # Si no existe la carpeta "out"
        os.makedirs('out') # Crea la carpeta "out"
    cv.imwrite("out/"+args["file"][:-4]+".png", output) # Guardar el output como un archivo .png en la carpeta creada
    
else: # Si el arguemtno "file" está en blanco
    variant = 0 # Efectos que se pueden aplicar al video
    blur = False
    script_start_time = time.time() # Inicializacion del cronometro del programa
    
    vid = cv.VideoCapture(int(args["cameraSource"]),cv.CAP_DSHOW) # Tomar control de la camara 
    
    #Loading Camera and Nose image and Creating mask
    l_image = cv.imread("lightning_emoji.png")
    success, frame = vid.read()
    rens = frame.shape[1]
    cols = frame.shape[0]
    face_mask = numpy.zeros((rens,cols), numpy.uint8)

    #Loading Face Detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
      
    while(vid.isOpened()): # Mientras la camara este en uso
        success, frame = vid.read() # Capturar el frame de la camara
        
        if not success: # Si la camara no es capaz de capturar el frame 
            continue # Reintetar
        if frame is None: # Si el frame el nulo
            continue # Reintentar
        
        if(blur): # Si blur es verdadero
            frame = cv.medianBlur(frame, 5) # Aplicar el efecto de Kernel de la mediana para reducir el ruido
        
        if(variant % 4 == 0): # Imagen original
            kernel = numpy.array(([0, 0, 0], [0, 1, 0], [0, 0, 0]), numpy.float32) # Sin tomar en cuenta pixeles aledaños
            output = cv.filter2D(frame, -1, kernel) # Aplicar Kernel de identidad en la imagen
            output = cv.putText(output,'Original',(20,30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),2)
        elif(variant % 4 == 1): # Convolucion, operador Sobel
            # Toma en cuenta los piexeles de derecha e izquierda, y los resta
            kernelx = numpy.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]), numpy.float32)
            # Toma en cuenta los piexeles de arriba y abajo, y los resta
            kernely = numpy.array(([-1, -2, -1], [0, 0, 0], [1, 2, 1]), numpy.float32)
            
            # Aplicar filtro de convolucion
            outputx = cv.filter2D(frame, -1, kernelx)
            outputy = cv.filter2D(frame, -1, kernely)
            
            output = cv.add(outputx, outputy) # Suma aritmetica de las imagenes
            output = cv.putText(output,'Sobel',(20,30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255),2)
            
        elif(variant % 4 == 2): # Aumentar la saturacion de la imagen
            kernel = numpy.array(([0, 1, 0], [1, 1, 1], [0, 1, 0]), numpy.float32) # Satura el pixel del centro con los pixeles aledaños
            output = cv.filter2D(frame, -1, kernel) # Aplicar filtro de saturación
            output = cv.putText(output,'Saturacion',(20,30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),2)
            
        else:
            face_mask.fill(0)
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = detector(frame)
            output = face_tracker(frame, l_image,rens,cols,face_mask, detector, predictor, gray_frame, faces)
            output = cv.putText(output,'Rayito emprendedor',(20,30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0),2)
            #print(output.shape)
        
        output = cv.putText(output,'Espacio - Cambiar filtro',(18,cols-18), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0),1)
        output = cv.putText(output,'Espacio - Cambiar filtro',(20,cols-20), cv.FONT_HERSHEY_PLAIN, 1, (255,255,255),1)
        
        output = cv.putText(output,'B - Reduccion de ruido',(18,cols-38), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0),1)
        
        if(blur):
            output = cv.putText(output,'B - Reduccion de ruido',(20,cols-40), cv.FONT_HERSHEY_PLAIN, 1, (70,255,70),1)
            
        else:
            output = cv.putText(output,'B - Reduccion de ruido',(20,cols-40), cv.FONT_HERSHEY_PLAIN, 1, (20,20,255),1)
      
        if variant % 4 == 1:
            output = cv.putText(output,'Esc - Salir',(rens-100,20), cv.FONT_HERSHEY_PLAIN, 1, (255,255,255),1)
        else:
            output = cv.putText(output,'Esc - Salir',(rens-100,20), cv.FONT_HERSHEY_PLAIN, 1, (0,0,0),1)
        
        if(frame is None):
            continue
        cv.imshow('frame', output) # Mostrar output en una ventana adicional
        
        k = cv.waitKey(10)
        if k == 27: # Cuando se pulsa esc.
            break
        elif k == 98: # Cuando se pulsa "b" 
            if blur:
                blur = False
            else:
                blur = True
        elif k == 32: # Cuando se pulsa espacio
            variant+=1
            
    vid.release() # Ceder el control de la camara
    cv.destroyAllWindows() # Terminar todas las ventanas
    
    
    print('Script took %f seconds.' % (time.time() - script_start_time)) # Mostar la duracion de la ejecucion del programa
