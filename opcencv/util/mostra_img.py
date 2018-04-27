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
img = imread(io.BytesIO(base64.b64decode(data["face"]["data"])))

# finally convert RGB image to BGR for opencv
# and save result
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
