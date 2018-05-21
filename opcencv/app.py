
from pprint import pprint
import numpy as np
import cv2
import matplotlib.pyplot as plt
from Cor import Cor
from Lib import Filtra_Contorno,get_Image,crop_imagem,Blur,Aplica_Filtros,Plota

imgs = []
# Define imagem do arquivo data.json
"""
imgs.append("IMG1")
imgs.append("IMG2")
imgs.append("face")
imgs.append("Resistor_Real")
imgs.append("RR_GIF")
imgs.append("RR2")
imgs.append("RR_JPG")
imgs.append("resistor")
imgs.append('R12K')
"""
imgs.append("resistor")
imgs.append('R12K')
imgs.append('R10K')

index=1
cnt=1
for img in imgs:
    # Decodifica imagem de base64 e le em formato cv2
    rgb = get_Image(img)

    # Filtra os contornos do resistor
    im2,contours,h,edges,closed = Filtra_Contorno(rgb)

    # Faz Bitwise and com mascara filtrada e redimensiona com parte util
    croped = crop_imagem(rgb,edges,closed)

    # Uniformiza cores para melhorar filtragem
    frame = Blur(croped)

    #Plota imagem
    index,cnt = Plota(imgs,index,cnt,rgb,frame)
    
plt.show()

print('End')
