import matplotlib.pyplot as plt
import copy
from Lib import Filtra_Contorno, get_Image, crop_imagem, Blur,Aplica_Filtros,Plota_Corte,Plota_Histogramas
from processa import Pega_Histogramas,Filtra_Histogramas,Filtra_Faixas
imgs = []
# Define imagens
#"""
imgs.append("R1.2") #BOM
imgs.append("R270")     #Melhor
imgs.append('R12K')
#"""
imgs.append('R10K')
#"""
imgs.append('330K')
imgs.append('120K')
imgs.append('150K')
imgs.append('180K')
#"""

index=1
plots=[]
for img in imgs:
    print('\n\n',img)
    # Decodifica imagem de base64 e le em formato cv2
    rgb = get_Image(img)

    # Filtra os contornos do resistor
    im2,contours,h,edges,closed = Filtra_Contorno(rgb)

    # Faz Bitwise and com mascara filtrada e redimensiona com parte util
    crop_mask,crop_img = crop_imagem(rgb,edges,closed)

    # Uniformiza cores para melhorar filtragem
    frame = Blur(crop_img)

    Cores = Aplica_Filtros(frame)

    Histogramas  = Pega_Histogramas(Cores)

    paleta  = Filtra_Histogramas(Histogramas)

    Faixas,valor = Filtra_Faixas(paleta)
    plot ={
    "img":copy.deepcopy(img),"rgb":copy.deepcopy(rgb),"edges":copy.deepcopy(edges),"crop_mask":copy.deepcopy(crop_mask),
    "frame":copy.deepcopy(frame),"Histogramas":copy.deepcopy(Histogramas),"paleta":copy.deepcopy(paleta),"valor":copy.deepcopy(valor)
    }
    plots.append(plot)

    #index = Plota(img,imgs,index,rgb,edges,crop_mask,frame,Histogramas,paleta.Cores,valor)

index=1
rows = 4
#"""
for plot in plots:
    index = Plota_Corte(plot['img'],plot['rgb'],plot['edges'],plot['crop_mask'],plot['frame'],index,rows)
    if(index>=rows*4):
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98,
                    wspace=0.3, hspace=0.3)
        plt.show()
        index=1
if(index>1):
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98,
                wspace=0.3, hspace=0.3)
    plt.show()
#"""
index=1
for plot in plots:
    #"img":img,"frame":frame,"Histogramas":Histogramas,"paleta":paleta,"valor":valor
    index = Plota_Histogramas(plot['img'],plot['frame'],plot['Histogramas'],plot['paleta'],plot['valor'],index,rows)
    if(index>=rows*4):
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98,
                    wspace=0.3, hspace=0.3)
        plt.show()
        index=1

if(index>1):
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98,
                wspace=0.3, hspace=0.3)
    plt.show()




print('End')
