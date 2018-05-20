
from pprint import pprint
import numpy as np
import cv2
import matplotlib.pyplot as plt
from Cor import Cor
from Lib import Filtra_Contorno,get_Image,crop_imagem

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
imgs.append('R10K')
for img in imgs:
    # Decodifica imagem de base64 e lê em formato cv2
    rgb = get_Image(img)

    im2,contours,h,edges,closed = Filtra_Contorno(rgb)

    croped = crop_imagem(rgb,edges,closed)


    #Definindo ranges de cores dos resistores
    l=[]
    l.append(Cor(0,"Preto",[16, 0, 0],[30, 163, 165]))
    l.append(Cor(1,"Marrom",[7, 61, 119],[12, 127, 210]))
    l.append(Cor(1,"Marrom2",[4, 61, 119],[7, 127, 210]))
    l.append(Cor(3,"Laranja",[10, 81, 178],[13, 164, 238]))
    #l.append(Cor(4,"Amarelo",[20, 130, 100],[30, 250, 160]))
    #l.append(Cor(5,"Verde",[45, 50, 60],[72, 250, 150]))
    #l.append(Cor(6,"Azul",[80, 50, 50],[106, 250, 150]))
    #l.append(Cor(7,"Roxo",[130, 40, 50],[155, 250, 150]))
    #l.append(Cor(8,"Cinza",[0,0, 50],[180, 50, 80]))
    #l.append(Cor(9,"Branco",[0, 0, 90],[180, 15, 140]))
    #l.append(Cor(2,"Vermelho1",[0, 76, 45],[7, 255, 2555]))
    #l.append(Cor(2,"Vermelho2",[170, 65, 102],[180, 255, 255]))


    #frame = median = cv2.medianBlur(crop_img,5)
    frame = croped
    #frame = cv2.GaussianBlur(frame,(5,5),cv2.BORDER_DEFAULT)   #1.71%
    frame = cv2.bilateralFilter(frame,9,75,75)                  #3.51%
    frame = median = cv2.medianBlur(frame,3)                   #3.07%
    #frame = cv2.blur(frame,(5,5))                              #1.51%

    # Convert BGR to HSV

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    plt.subplot(len(l)+1,2,1),plt.imshow(rgb,cmap = 'gray')
    plt.title(img+'Original'), plt.xticks([]), plt.yticks([])
    plt.subplot(len(l)+1,2,2),plt.imshow(frame,cmap = 'gray')
    plt.title('recortada'), plt.xticks([]), plt.yticks([])
    cv2.imwrite( '/app_saves/recortada.jpg', frame )

    #Atualiza dimensão da imagem cortada para saber % de cada cor
    height, width,layers = frame.shape
    frm_cnt = 3
    for color in l:
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

print('End')
#Espera fechar janelas para encerrar o processo, não pode ter isso no código final
#cv2.waitKey(0)
#cv2.destroyAllWindows()
