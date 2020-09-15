import numpy
import cv2 as cv
import matplotlib.pyplot as plt

image = cv.imread("sample.png")
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

kernelx = numpy.array(([-1,0,1],[-2,0,2],[-1,0,1]),numpy.float32)
kernely = numpy.array(([-1,-2,-1],[0,0,0],[1,2,1]),numpy.float32)

kernel = numpy.array(([2,4,2],[4,8,4],[2,4,2]),numpy.float32)

outputMx = cv.filter2D(image, -1, kernelx)
outputMy = cv.filter2D(image, -1, kernely)

output = cv.filter2D(image, -1, kernel)

plt.subplot(2,2,1)
plt.imshow(image)
plt.title('Original Image')

plt.subplot(2,2,2)
plt.imshow(outputMx)
plt.title("Filtered Image X")

plt.subplot(2,2,3)
plt.imshow(outputMy)
plt.title("Filtered Image Y")

plt.subplot(2,2,4)
plt.imshow(output)
plt.title("Filtered Image XxY")

plt.savefig('out.png')
