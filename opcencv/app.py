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

##################
IS_FOUND = 0

MORPH = 7
CANNY = 250
##################
# 420x600 oranı 105mmx150mm gerçek boyuttaki kağıt için
_width  = 600.0
_height = 420.0
_margin = 0.0
##################

# Define imagem do arquivo data.json
Imagem="RR_JPG"
# importa arquivo data.json
data = json.load(open('data.json'))

# Decodifica imagem de base64 e lê em formato cv2
rgb = imread(io.BytesIO(base64.b64decode(data[Imagem]["data"])))

# Aplica escala de cinza na imagem
gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )
gray = cv2.bilateralFilter( gray, 1, 10, 120 )

# Detecta edges na  imagem
edges  = cv2.Canny(gray, 10,CANNY )

# Não sei o que essa parada faz
kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )
closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

# Essa função acha os contornos
im2,contours,h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )

#Faz loop na imagem e pinta de branco os contornos
for cont in contours:

    if cv2.contourArea( cont ) > 5000 :

        arc_len = cv2.arcLength( cont, True )
        approx = cv2.approxPolyDP( cont, 0.1 * arc_len, True )
        if ( len( approx ) == 4 ):
            IS_FOUND = 1
            pts_src = np.array( approx, np.float32 )
            h, status = cv2.findHomography( pts_src, pts_dst )
            out = cv2.warpPerspective( rgb, h, ( int( _width + _margin * 2 ), int( _height + _margin * 2 ) ) )

            cv2.drawContours( rgb, [approx], -1, ( 255, 0, 0 ), 2 )

        else : pass

#Faz plot dos resultados

plt.subplot(2,2,1),plt.imshow(rgb,cmap = 'gray')
plt.title('rgb'), plt.xticks([]), plt.yticks([])
cv2.imwrite( 'rgb.jpg', rgb )

plt.subplot(2,2,2),plt.imshow(gray,cmap = 'gray')
plt.title('gray'), plt.xticks([]), plt.yticks([])
cv2.imwrite( 'gray.jpg', gray )

plt.subplot(2,2,3),plt.imshow(edges,cmap = 'gray')
plt.title('edges'), plt.xticks([]), plt.yticks([])
cv2.imwrite( 'edges.jpg', edges )

plt.subplot(2,2,4),plt.imshow(closed,cmap = 'gray')
plt.title('closed'), plt.xticks([]), plt.yticks([])
cv2.imwrite( 'closed.jpg', closed )

plt.show()

if IS_FOUND :
    cv2.namedWindow( 'out')
    cv2.imshow( 'out', out )


#Faz print no console
print("Pictures saved")
print('End')

#Espera fechar janelas para encerrar o processo, não pode ter isso no código final
#cv2.waitKey(0)
#cv2.destroyAllWindows()
