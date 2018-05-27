import cv2
from operator import attrgetter
import numpy as np
import peakutils
import math
from scipy.signal import butter, lfilter, find_peaks_cwt
from Cor import Pico,Faixa

def Analisa_Mascaras(Cores):
    for cor in Cores:
        h,w = cor.Mask.shape
        cor.media =  cv2.countNonZero(cor.Mask)/w
    Cores.sort(key=attrgetter('media'),reverse=True)# Ordena cores por percentual na foto
    media_top3 = (Cores[0].media+Cores[1].media+Cores[2].media)/3
    top = []
    for cor in Cores:
        if(cor.media>=media_top3*0.3):
            top.append(cor)
    media_Top = 0 # Media de pixels das cores que mais significantes
    for cor in top:
        media_Top+= cor.media
    media_Top = media_Top/6
    maior_pico = 0
    Top_com_Picos=[]
    for cor in top:
        histograma = []
        mediana = []
        h,w = cor.Mask.shape
        k = w%2 # =0 se par e 1 se impar
        for x in range(0,w-k,2):
            valor = cv2.countNonZero(cor.Mask[0:h,x:x+1])
            histograma.append(valor)
            mediana.append(cor.media)
        cor.histograma = histograma
        cor.mediana = mediana
        #Filtro passa baixa butterworth
        cor.histograma_Filtrado = butter_lowpass_filter(histograma,2,50, order=10)
        #Encontra indices dos picos filtrados
        indices = peakutils.indexes(cor.histograma_Filtrado, thres=0.02/max(cor.histograma_Filtrado), min_dist=0.1)
        cor.picos=[]
        #Filtra picos significativos
        for indice in indices:
            if(cor.histograma_Filtrado[indice]>2.5*media_Top):
                cor.picos.append(indice)
                if(cor.histograma_Filtrado[indice]>maior_pico):
                    maior_pico=cor.histograma_Filtrado[indice]
    maior_indice=0
    menor_indice=9999999999

    #print('Entrada')
    #Imprime_Picos(top)

    #Remove picos menores que 20% do maior pico
    for cor in top:
        picos = cor.picos
        cor.picos = []
        for indice in picos:
            if(cor.histograma_Filtrado[indice]>0.2*maior_pico):
                cor.picos.append(indice)
                if(indice>maior_indice):
                    maior_indice = indice
                if(indice<menor_indice):
                    menor_indice = indice
        if(len(cor.picos)>0):
            Top_com_Picos.append(cor)
    top = Top_com_Picos
    delta = maior_indice-menor_indice
    tolerancia = 0.15*delta
    #if (tolerancia<5):
    #   tolerancia=5
    #print('\n(Menor,Maior,Delta,tolerancia)',(menor_indice,maior_indice,delta,tolerancia))

    #remove picos repetidos e deixa o mair pico
    Top_filtrado = []
    Faixas =[]
    for cor in top:
        Maiores_Picos =[]
        for pico in cor.picos:
            append = True
            for cor2 in top:
                #print('\n',cor.nome,'\tX\t',cor2.nome)
                if(cor != cor2):
                    for pico2 in cor2.picos:
                        delta = pico-pico2
                        if(delta<0):
                            delta = delta*(-1)
                        #print('(delta,tolerancia,(p1,Vp1),(p2,Vp2))',(delta,tolerancia,(pico,cor.histograma_Filtrado[pico]),(pico2,cor2.histograma_Filtrado[pico2])))
                        if(delta<=tolerancia and cor.histograma_Filtrado[pico]<cor2.histograma_Filtrado[pico2]):
                            append = False
            if(append):
                Maiores_Picos.append(pico)
                Faixas.append(Faixa(cor.nome,cor.histograma_Filtrado[pico],pico))
        if(len(Maiores_Picos)>0):
            cor.picos = Maiores_Picos
            Top_filtrado.append(cor)
    top = Top_filtrado
    #print('\nSaida:')
    Faixas.sort(key=attrgetter('indice'),reverse=False)
    Imprime_Faixas(Faixas)
    valor = Pega_Valor(Faixas)
    return top

def Pega_Valor(Faixas):
    o=0

def Imprime_Picos(Cores):
    for cor in Cores:
        print('\n',cor.nome,'\t\tPicos:',cor.picos)#,'\tN:',len(cor.picos))
def Imprime_Faixas(Faixas):
    for faixa in Faixas:
        print('\n',faixa.cor,'\t\tIndice:',faixa.indice,'\tH:',faixa.valor)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
