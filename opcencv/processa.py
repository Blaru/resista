import cv2
from operator import attrgetter
import numpy as np
import peakutils
from scipy.signal import butter, lfilter, find_peaks_cwt
from Cor import Pico

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
        cor.picos = []
        #Filtra picos significativos
        for indice in indices:
            if(cor.histograma_Filtrado[indice]>5*media_Top):
                cor.picos.append(indice)
    #remove cores sem picos nas cores represntativas
    Top_filtrado = []
    for cor in top:
        if (len(cor.picos)>0):
            Top_filtrado.append(cor)
            print(cor.nome,'\t\tPicos:',cor.picos,'\tN:',len(cor.picos))


    return top

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
