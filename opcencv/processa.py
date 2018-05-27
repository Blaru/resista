import cv2
import numpy as np
from scipy.signal import butter, lfilter, find_peaks_cwt
from Cor import Pico

def Analisa_Mascaras(Cores):
    histogramas = []
    media_cores = 0
    Ncores=0
    for cor in Cores:
        Ncores+=1
        media = []
        h,w = cor.Mask.shape
        cor.media =  cv2.countNonZero(cor.Mask)/w
        media_cores+=cor.media
    media_cores = media_cores/Ncores
    for cor in Cores:
        histograma = []
        mediana = []
        h,w = cor.Mask.shape
        k = w%2 # =0 se par e 1 se impar
        Pico_Mais_Alto=0
        X_pico_do_pico = 0
        pico_do_pico =0
        dentro_do_pico = False
        inicio_do_pico=0
        minimo = 4*media_cores
        for x in range(0,w-k,2):
            valor = cv2.countNonZero(cor.Mask[0:h,x:x+1])
            histograma.append(valor)
            mediana.append(cor.media)
        cor.histograma_Filtrado = butter_lowpass_filter(histograma,2,50, order=6)
        for valor in cor.histograma_Filtrado:
            if(valor>Pico_Mais_Alto):
                Pico_Mais_Alto = valor
            if(valor>pico_do_pico):
                X_pico_do_pico = valor
            if(dentro_do_pico==False and valor > minimo):
                dentro_do_pico=True
                inicio_do_pico=x
            if(dentro_do_pico and valor<minimo):
                cor.Picos.append( Pico(inicio_do_pico,x,X_pico_do_pico) )
                dentro_do_pico=False
                pico_do_pico =0
        Pn=0
        print('Cor:',cor.nome)
        for pico in cor.Picos:
            Pn+=1
            print('Inicio:',pico.inicio,'fim:',pico.fim,'largura:',pico.largura,'pto_alto:',pico.pto_alto)
        cor.Pico_Mais_Alto = Pico_Mais_Alto
        cor.histograma = histograma
        cor.mediana = mediana
    return Cores

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
