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

MORPH = 51
CANNY = 255
##################
# 420x600 oranı 105mmx150mm gerçek boyuttaki kağıt için
_width  = 600.0
_height = 420.0
_margin = 0.0
##################

# Define imagem do arquivo data.json
#Imagem ="RR2"
#Imagem = "RR_JPG"
Imagem = 'R12K'
#Imagem = 'R22K'
#Imagem = 'R10K'

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
"""
#Faz plot dos resultados de edge
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

#plt.show()
"""

if IS_FOUND :
    cv2.namedWindow( 'out')
    cv2.imshow( 'out', out )

#Faz print no console
print("Pictures saved")

print('rgb Dimensions:\t' ,rgb.shape)
print('Edges Dimensions:\t' ,edges.shape)

height, width,layers = rgb.shape


#Esse bloco vai varrer para pegar o retangulo util do contorno
#edges[503][221]
#edges[row][colum]
encontrou = 0
for x in range(0, height):
    if (encontrou==1):
        break
    for y in range(0, width):
        #print("Superior esquerdo:\t",x,':',y)
        if(edges[x][y]==255):
            SE = (x,y)
            print("Superior esquerdo:\t",SE)
            encontrou =1
            break

encontrou = 0
for x in range(height-1,0,-1):
    if (encontrou==1):
        break
    for y in range(width-1,0,-1):
        #print("Inferior esquerdo:\t",x,':',y)
        if(edges[x][y]==255):
            ID = (x,y)
            print("Inferior Direito:\t",ID)
            encontrou =1
            break

#Calcula Altura e Largura  do crop para processar
h = ID[0]-SE[0]
w = ID[1]-SE[1]
print('Altura:\t',h)
print('Largura:\t',w)
#crop_img = img[y:y+h, x:x+w]
res = cv2.bitwise_and(rgb,rgb, mask= closed)
crop_img = res[SE[0]:ID[0], SE[1]:ID[1]]

#Definindo classes de cores dos resistores
class Cor_Resistor(object):
    def __init__(self, valor, nome, lower, upper):
        self.valor = valor
        self.nome = nome
        self.lower = np.array(lower)
        self.upper = np.array(upper)

#Definindo ranges de cores dos resistores
l=[]
#l.append(Cor_Resistor(0,"Preto",[0, 0, 0],[180, 250, 50]))
l.append(Cor_Resistor(1,"Marrom",[0, 102, 0],[16, 255, 75]))
l.append(Cor_Resistor(3,"Laranja",[9, 100, 80],[11, 255, 255]))
#l.append(Cor_Resistor(4,"Amarelo",[20, 130, 100],[30, 250, 160]))
#l.append(Cor_Resistor(5,"Verde",[45, 50, 60],[72, 250, 150]))
#l.append(Cor_Resistor(6,"Azul",[80, 50, 50],[106, 250, 150]))
#l.append(Cor_Resistor(7,"Roxo",[130, 40, 50],[155, 250, 150]))
#l.append(Cor_Resistor(8,"Cinza",[0,0, 50],[180, 50, 80]))
#l.append(Cor_Resistor(9,"Branco",[0, 0, 90],[180, 15, 140]))
l.append(Cor_Resistor(2,"Vermelho1",[0, 76, 45],[7, 255, 2555]))
#l.append(Cor_Resistor(2,"Vermelho2",[170, 65, 102],[180, 255, 255]))

plt.subplot(len(l)+1,2,1),plt.imshow(rgb,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(len(l)+1,2,2),plt.imshow(crop_img,cmap = 'gray')
plt.title('recortada'), plt.xticks([]), plt.yticks([])
cv2.imwrite( '/app_saves/recortada.jpg', crop_img )

frame = crop_img
# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
contador = 3
for color in l:
    mask = cv2.inRange(hsv, color.lower, color.upper)
    # Bitwise-AND Mascara e original
    res = cv2.bitwise_and(frame,frame, mask= mask)
    plt.subplot(len(l)+1,2,contador),plt.imshow(mask,cmap = 'gray')
    contador = contador+1
    plt.title(color.nome), plt.xticks([]), plt.yticks([])
    #cv2.imwrite(('/app_saves/'+color.nome+'mask.jpg'), mask)
    plt.subplot(len(l)+1,2,contador),plt.imshow(res,cmap = 'gray')
    contador = contador+1
    plt.title(color.nome), plt.xticks([]), plt.yticks([])
    #cv2.imwrite( ('/app_saves/'+color.nome+'res.jpg'), res )

plt.show()

print('End')
#Espera fechar janelas para encerrar o processo, não pode ter isso no código final
#cv2.waitKey(0)
#cv2.destroyAllWindows()
