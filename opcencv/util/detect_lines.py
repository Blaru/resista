import json
from pprint import pprint
import numpy as np
import base64
import io
import cv2
from imageio import imread
import matplotlib.pyplot as plt
# data["face"]["data"]
#
data = json.load(open('data.json'))
# reconstruct image as an numpy array
img = imread(io.BytesIO(base64.b64decode(data["resistorRot"]["data"])))

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 0
maxLineGap = 0
lines = cv2.HoughLinesP(edges,5,np.pi/180,100,minLineLength,maxLineGap)
print (lines)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines5.jpg',img)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
