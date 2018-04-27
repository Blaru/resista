import json
from pprint import pprint
import numpy as np
import base64
import io
import cv2
import imutils
import ShapeDetector
from imageio import imread
import matplotlib.pyplot as plt

# data["face"]["data"]
#
data = json.load(open('data.json'))
# reconstruct image as an numpy array
img = imread(io.BytesIO(base64.b64decode(data["resistorRot"]["data"])))
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = img
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
sd = ShapeDetector()
