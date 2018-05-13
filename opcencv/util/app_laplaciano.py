import json

from pprint import pprint

import numpy as np

import base64

import io

import cv2

from imageio import imread

from matplotlib import pyplot as plt



data = json.load(open('data.json'))


Imagem="RR_JPG"
# reconstruct image as an numpy array
#img = imread(io.BytesIO(base64.b64decode(data[Imagem]["data"])))
img = cv2.medianBlur(imread(io.BytesIO(base64.b64decode(data[Imagem]["data"]))),3)

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)


plt.subplot(2,3,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])


plt.subplot(2,3,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])


plt.subplot(2,3,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

plt.subplot(2,3,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

img = cv2.Laplacian(img,cv2.CV_64F)
tmp = cv2.resize(img, (480, 480)) # scaling
(rows, cols,qualquercoisa) = tmp.shape

M = np.float32([[1,0,100],[0,1,50]])
trans = cv2.warpAffine(tmp,M,(cols,rows)) # translation

plt.subplot(2,3,5),plt.imshow(trans,cmap = 'gray')
plt.title('trans'), plt.xticks([]), plt.yticks([])

trans2 = cv2.medianBlur(imread(io.BytesIO(base64.b64decode(data["Resistor_Real"]["data"]))),5)

plt.subplot(2,3,6),plt.imshow(trans2,cmap = 'gray')
plt.title('trans2'), plt.xticks([]), plt.yticks([])

plt.show()
