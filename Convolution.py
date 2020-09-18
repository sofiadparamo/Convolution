import numpy 
import cv2 as cv
import argparse
import os
import time

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
    
    vid = cv.VideoCapture(int(args["cameraSource"])) # Tomar control de la camara 
      
    while(vid.isOpened()): # Mientras la camara este en uso
        success, frame = vid.read() # Capturar el frame de la camara
        
        if not success: # Si la camara no es capaz de capturar el frame 
            continue # Reintetar
        if frame is None: # Si el frame el nulo
            continue # Reintentar
        
        if(blur): # Si blur es verdadero
            frame = cv.medianBlur(frame, 5) # Aplicar el efecto de Kernel de la mediana para reducir el ruido
        
        if(variant % 3 == 0): # Imagen original
            kernel = numpy.array(([0, 0, 0], [0, 1, 0], [0, 0, 0]), numpy.float32) # Sin tomar en cuenta pixeles aledaños
            output = cv.filter2D(frame, -1, kernel) # Aplicar Kernel de identidad en la imagen
            
        elif(variant % 3 == 1): # Convolucion, operador Sobel
            # Toma en cuenta los piexeles de derecha e izquierda, y los resta
            kernelx = numpy.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]), numpy.float32)
            # Toma en cuenta los piexeles de arriba y abajo, y los resta
            kernely = numpy.array(([-1, -2, -1], [0, 0, 0], [1, 2, 1]), numpy.float32)
            
            # Aplicar filtro de convolucion
            outputx = cv.filter2D(frame, -1, kernelx)
            outputy = cv.filter2D(frame, -1, kernely)
            
            output = cv.add(outputx, outputy) # Suma aritmetica de las imagenes
            
        elif(variant % 3 == 2): # Aumentar la saturacion de la imagen
            kernel = numpy.array(([0, 1, 0], [1, 1, 1], [0, 1, 0]), numpy.float32) # Satura el pixel del centro con los pixeles aledaños
            output = cv.filter2D(frame, -1, kernel) # Aplicar filtro de saturación
      
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
