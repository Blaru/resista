#Imports para OpenCV
import numpy as np
import cv2
import matplotlib.pyplot as plt
#Imports para Base64 e JSON
import json
from imageio import imread
import io
import base64
#import para processamento de sinal
from scipy import signal
from scipy.signal import butter, lfilter
#################
#Bibliotecas próprias
from processa import butter_lowpass_filter
from cores import Cores
from Cor import Pico
##################
from plot_Histograma import plot_Histograma
#Variaveis Para Function Filtra_Contorno
CANNY = 255
##################
# importa arquivo data.json
data = json.load(open('data.json'))
def get_Image(nome):
    return imread(io.BytesIO(base64.b64decode(data[nome]["data"])))

def Filtra_Contorno(rgb):
    h,w,s = rgb.shape
    # Aplica escala de cinza na imagem
    gray = cv2.cvtColor( rgb, cv2.COLOR_BGR2GRAY )
    gray = cv2.bilateralFilter( gray, 1, 10, 120 )
    # Detecta edges na  imagem
    edges  = cv2.Canny(gray, 10,CANNY )
    # Nao sei o que essa parada faz
    kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( int(w/2), int(h/2) ) )
    closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )
    # Essa funco acha os contornos
    im2,contours,h = cv2.findContours( closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    return [im2,contours,h,edges,closed]

def crop_imagem(rgb,edges,closed):
    x,y,w,h = cv2.boundingRect(edges)
    return [edges[y:y+h,x:x+w],rgb[y:y+h,x:x+w]]

def Blur(img):
    h,w,s = img.shape
    #blur
    #GaussianBlur
    img = cv2.bilateralFilter(img,9,75,75)                  #3.51%
    img = cv2.GaussianBlur(img,(5,5),0)
    img = cv2.medianBlur(img,3)                   #3.07%
    return img

def Aplica_Filtros(frame):
    # Converte RGB to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    #Atualiza dimensao da imagem cortada para saber % de cada cor
    h, w,layers = frame.shape
    index=0
    for cor in Cores:
        Mask = 1
        del Mask
        #print ('Cor:\t'+cor.nome)
        for filtro in cor.Filtros:
            try:
                Mask
            except NameError:
                Mask = cv2.inRange(hsv, filtro.lower, filtro.upper)
                #print ('Undefined\t'+str(cv2.countNonZero(Mask)))
            else:
                mask = cv2.inRange(hsv, filtro.lower, filtro.upper)
                Mask = cv2.bitwise_or(mask,Mask)      # Bitwise-AND Mascara e original
                #print ('defined\t'+str(cv2.countNonZero(mask)))
        cor.mask_cnt = cv2.countNonZero(Mask)
        cor.mask_percent = (cv2.countNonZero(Mask)/(h*w))*100
        cor.Mask = Mask
        #print ('Final\t'+str(cv2.countNonZero(Mask)))
        h,w,s = frame.shape
        filtrado  = cv2.bitwise_and(frame,frame, mask= Mask)
    return Cores

def Plota(img,imgs,index,rgb,edges,crop_mask,frame,Cores):
    size = len(imgs)
    #print('size:',size,',5,index:',index)

    plt.subplot(size,3,index),plt.imshow(frame,cmap = 'gray')
    plt.title('frame'), plt.xticks([]), plt.yticks([])

    plt.subplot(size,3,index+1)
    plt.title('Histograma')
    h,w = crop_mask.shape
    plot_Histograma(plt,h,w,Cores)

    plt.subplot(size,3,index+2)
    plt.title('Filtrado')
    h,w = crop_mask.shape
    plot_Histograma(plt,h,w,Cores,Filtrado=True)

    index+=3
    return index
