
from pprint import pprint
import numpy as np
import cv2
import matplotlib.pyplot as plt
from Cor import Cor
from Lib import Filtra_Contorno, get_Image, crop_imagem, Blur,Aplica_Filtros, Plota
imgs = []
# Define imagens
imgs.append("Resistor_Real")
#"""
imgs.append("resistor")
imgs.append('R12K')
imgs.append('R10K')
imgs.append('330K')
imgs.append('120K')
imgs.append('150K')
imgs.append('180K')#"""

index=1
cnt=1
for img in imgs:
    print('\n',img,'\n')
    # Decodifica imagem de base64 e le em formato cv2
    rgb = get_Image(img)

    # Filtra os contornos do resistor
    im2,contours,h,edges,closed = Filtra_Contorno(rgb)

    # Faz Bitwise and com mascara filtrada e redimensiona com parte util
    crop_mask,crop_img,fail = crop_imagem(rgb,edges,closed)

    # Uniformiza cores para melhorar filtragem
    frame = Blur(crop_img)
    Aplica_Filtros(frame)
    #Plota imagem
    #index,cnt = Plota(imgs,index,cnt,rgb,edges,crop_mask,frame,img)

#plt.show()

print('End')
