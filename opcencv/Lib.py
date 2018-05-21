#Imports para OpenCV
import numpy as np
import cv2
import matplotlib.pyplot as plt
#Imports para Base64 e JSON
import json
from imageio import imread
import io
import base64
from cores import Cores
##################
#Variaveis Para Function Filtra_Contorno
IS_FOUND = 0
MORPH = 121
CANNY = 255
_width  = 600.0
_height = 420.0
_margin = 5
##################
# importa arquivo data.json
data = json.load(open('data.json'))
def get_Image(nome):
    return imread(io.BytesIO(base64.b64decode(data[nome]["data"])))

def Filtra_Contorno(rgb):
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
    return [im2,contours,h,edges,closed]

def crop_imagem(rgb,edges,closed):
    print('rgb Dimensions:\t' ,rgb.shape)
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
    return crop_img

def Blur(img):
    frame = img
    #frame = cv2.GaussianBlur(frame,(5,5),cv2.BORDER_DEFAULT)   #1.71%
    #frame = cv2.blur(frame,(5,5))                              #1.51%
    #frame = median = cv2.medianBlur(crop_img,5)
    frame = cv2.bilateralFilter(frame,9,75,75)                  #3.51%
    frame = cv2.medianBlur(frame,3)                   #3.07%
    return frame

def Aplica_Filtros(frame):
    # Converte RGB to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    plt.subplot(len(l)+1,2,1),plt.imshow(rgb,cmap = 'gray')
    plt.title(img+'Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(len(l)+1,2,2),plt.imshow(frame,cmap = 'gray')
    plt.title('recortada'), plt.xticks([]), plt.yticks([])
    cv2.imwrite( '/app_saves/recortada.jpg', frame )

    #Atualiza dimensão da imagem cortada para saber % de cada cor
    height, width,layers = frame.shape
    frm_cnt = 3
    for cor in Cores:
        mask = cv2.inRange(hsv, color.lower, color.upper)
        res = cv2.bitwise_and(frame,frame, mask= mask)  # Bitwise-AND Mascara e original

        plt.subplot(len(l)+1,2,frm_cnt),plt.imshow(mask,cmap = 'gray')
        percent = (cv2.countNonZero(mask)/(height*width))*100
        plt.title(color.nome+'('+str(percent)+'%)'), plt.xticks([]), plt.yticks([])
        #cv2.imwrite(('/app_saves/'+color.nome+'mask.jpg'), mask)
        frm_cnt = frm_cnt+1

        plt.subplot(len(l)+1,2,frm_cnt),plt.imshow(res,cmap = 'gray')
        plt.title(color.nome), plt.xticks([]), plt.yticks([])
        #cv2.imwrite( ('/app_saves/'+color.nome+'res.jpg'), res )
        frm_cnt = frm_cnt+1


    plt.show()
    
def Plota(imgs,index,cnt,rgb,frame):
    plt.subplot(len(imgs),2,index),plt.imshow(rgb,cmap = 'gray')
    plt.title('Original'), plt.xticks([]), plt.yticks([])
    index+=1
    plt.subplot(len(imgs),2,index),plt.imshow(frame,cmap = 'gray')
    plt.title('frame'), plt.xticks([]), plt.yticks([])
    cv2.imwrite(('/app_saves/frame'+str(cnt)+'.jpg'), frame)
    index+=1
    cnt += 1
    return [index,cnt]
