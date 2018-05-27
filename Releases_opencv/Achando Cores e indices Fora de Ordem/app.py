import matplotlib.pyplot as plt
from Lib import Filtra_Contorno, get_Image, crop_imagem, Blur,Aplica_Filtros,Plota
from processa import Analisa_Mascaras
imgs = []
# Define imagens
imgs.append("R1.2") #BOM
"""
imgs.append("R270")     #Melhor
imgs.append('R12K')

#imgs.append('R10K')
#"""
#"""
imgs.append('330K')
imgs.append('120K')
imgs.append('150K')
imgs.append('180K')
#"""

index=1
for img in imgs:
    print('\n',img,'\n')
    # Decodifica imagem de base64 e le em formato cv2
    rgb = get_Image(img)

    # Filtra os contornos do resistor
    im2,contours,h,edges,closed = Filtra_Contorno(rgb)

    # Faz Bitwise and com mascara filtrada e redimensiona com parte util
    crop_mask,crop_img = crop_imagem(rgb,edges,closed)

    # Uniformiza cores para melhorar filtragem
    frame = Blur(crop_img)

    Cores = Aplica_Filtros(frame)

    Cores  = Analisa_Mascaras(Cores)

    index = Plota(img,imgs,index,rgb,edges,crop_mask,frame,Cores)

plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.98,
                wspace=0.3, hspace=0.3)

plt.show()

print('End')
