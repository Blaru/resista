import sys
import copy
from Lib import Filtra_Contorno, get_Image_From_B64, crop_imagem, Blur,Aplica_Filtros
from processa import Pega_Histogramas,Filtra_Histogramas,Filtra_Faixas

def dummy() :
    img = str(sys.argv[2])
    print('argumento = ',img)
    File =  open("./photos/"+img+".txt","r")
    img = File.read()
    #print('oi,',img)

    rgb = get_Image_From_B64(img)

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

    print(valor)
if __name__ =='__main__' :
    dummy = dummy()
