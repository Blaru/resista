from operator import attrgetter
import numpy as np
import peakutils
import math
from si_prefix import si_format

from scipy.signal import butter, lfilter, find_peaks_cwt
from Cor import Pico,Faixa,Paleta
import cv2

def  Pega_Histogramas(Cores):
    for cor in Cores:
        histograma = []
        mediana = []
        h,w = cor.Mask.shape
        k = w%2 # =0 se par e 1 se impar
        for x in range(0,w-k,2):
            valor = cv2.countNonZero(cor.Mask[0:h,x:x+1])
            cor.media =  cv2.countNonZero(cor.Mask)/w
            histograma.append(valor)
            mediana.append(cor.media)
        cor.histograma = histograma
        cor.Todas_Cores_Filtradas = butter_lowpass_filter(cor.histograma,2,50, order=10)
        cor.mediana = mediana
    return Cores

def Filtra_Histogramas(Cores):
    paleta = Paleta()
    paleta.maior_pico = 0
    for cor in Cores:
        cor.histograma_Filtrado = cor.Todas_Cores_Filtradas
        if(max(cor.histograma_Filtrado)>paleta.maior_pico):
            paleta.maior_pico = max(cor.histograma_Filtrado)
    #print('Maior pico da foto:',paleta.maior_pico)
    paleta.Cores = []
    for cor in Cores:
        if(max(cor.histograma_Filtrado)>paleta.maior_pico*0.248):
            cor.picos = peakutils.indexes(cor.histograma_Filtrado, thres=0.02/max(cor.histograma_Filtrado), min_dist=0.1)
            #print('Cor:\t',cor.nome,'picos:',cor.picos)
            paleta.Cores.append(cor)
            #print(cor.nome,'__Mantida,max,limite',max(cor.histograma_Filtrado),paleta.maior_pico*0.248)
        #else:
            #print(cor.nome,'__Descartada,max,limite',max(cor.histograma_Filtrado),paleta.maior_pico*0.248)
    return paleta

def Media_Top(paleta):
    paleta.media_Top = 0 # Media de pixels das cores que mais significantes
    for cor in paleta.Cores:
        paleta.media_Top+= cor.media
    paleta.media_Top = paleta.media_Top/len(paleta.Cores)

def Pico_Utils(paleta):
    #   maior_pico  =>   maior_pico
    #   Ma_I        =>   maior_indice
    #   Me_I        =>   menor_indice
    #   delta       =>   DeltaX entre Primeiro e Ultimo Pico
    #   tolerancia  =>   0.15*DeltaX
    paleta.maior_pico
    paleta.Ma_I=0
    paleta.Me_I=9999999999
    for cor in paleta.Cores:
        #Filtra picos significativos
        for indice in cor.picos:
            if(indice>paleta.Ma_I):
                paleta.Ma_I = indice
            if(indice<paleta.Me_I):
                paleta.Me_I = indice
    paleta.delta = paleta.Ma_I-paleta.Me_I
    paleta.tolerancia = 0.15*paleta.delta

def Filtra_Picos(paleta):
    for cor in paleta.Cores:
        picos = cor.picos
        cor.picos = []
        for indice in picos:
            #print(cor.nome,'\nPico,0.2*MP\n',(cor.histograma_Filtrado[indice],0.1*paleta.maior_pico))
            acima_da_media_reduzida = cor.histograma_Filtrado[indice]>0.3*paleta.media_Top
            Maior_que_30percent_MP = cor.histograma_Filtrado[indice]>0.25*paleta.maior_pico
            #print('\nacima_da_media_reduzida:\t',acima_da_media_reduzida)
            #print('\Maior_que_30percent_MP:\t',Maior_que_30percent_MP)
            if(Maior_que_30percent_MP and acima_da_media_reduzida):
                cor.picos.append(indice)

def Remove_Picos_coincidentes(paleta):
    Faixas =[]
    for cor in paleta.Cores:
        Maiores_Picos =[]  #Variavel que filtra picos que sejam menores que outros de outras cores
        for pico in cor.picos:
            append = True   #Assume que esse pico o maior dessa faixa
            for cor2 in paleta.Cores:
                if(cor != cor2): #Nao compara picos da cor com ela mesma
                    for pico2 in cor2.picos:
                        #Compara o pico com todos os picos dessa cor
                        delta = pico-pico2 #Verifica
                        if(delta<0):
                            delta = delta*(-1)
                        #print('(delta,tolerancia,(p1,Vp1),(p2,Vp2))',(delta,tolerancia,(pico,cor.histograma_Filtrado[pico]),(pico2,cor2.histograma_Filtrado[pico2])))
                        if(delta<=paleta.tolerancia and cor.histograma_Filtrado[pico]<cor2.histograma_Filtrado[pico2]):
                            #Encontramos um pico dentro da tolerancia que  maior que o pico em analise
                            append = False
            if(append):
                Maiores_Picos.append(pico)
                Faixas.append(Faixa(cor.nome,cor.valor,pico))
        if(len(Maiores_Picos)>0):
            cor.picos = Maiores_Picos
    return Faixas

def Filtra_Faixas(paleta):
    #Array com as cores que tem representatividade na foto, media > 10% da media das 3 maiores

    #Encontra a media do percentual de pixels das cores
    Media_Top(paleta)

    #Remove picos menores que 30% do maior pico e <25% da media
    Filtra_Picos(paleta)

    Pico_Utils(paleta)

    #print('\n(Menor,Maior,Delta,tolerancia)',(paleta.Me_I,paleta.Ma_I,paleta.delta,paleta.tolerancia))

    #remove picos repetidos e deixa o mair pico
    Faixas = Remove_Picos_coincidentes(paleta)

    Faixas.sort(key=attrgetter('indice'),reverse=False)
    #Imprime_Faixas(Faixas)

    valor = Pega_Valor(Faixas)

    return [Faixas,valor]
    #"""

def Pega_Valor(Faixas):
    DIM = len(Faixas)
    #print('DIM___',len(Faixas))
    if(DIM<3 or DIM>6):
        #print('Invalido__ Faixas:',len(Faixas))
        return 'Tente Novamente'
    else:
        if(DIM == 3):
            #print('Caso 3,(0,1,2)=',(Faixas[0].valor,Faixas[1].valor,Faixas[2].valor))
            return str(si_format(int(float(str(Faixas[0].valor)+str(Faixas[1].valor)+'E'+str(Faixas[2].valor)))))
        elif(DIM == 4):
            return str(si_format(int(float(str(Faixas[0].valor)+str(Faixas[1].valor)+str(Faixas[2].valor)+'E'+str(Faixas[3].valor)))))
        elif(DIM == 5):
            return str(si_format(int(float(str(Faixas[0].valor)+str(Faixas[1].valor)+str(Faixas[2].valor)+str(Faixas[3].valor)+'E'+str(Faixas[4].valor)))))
        elif(DIM == 6):
            return str(si_format(int(float(str(Faixas[0].valor)+str(Faixas[1].valor)+str(Faixas[2].valor)+str(Faixas[3].valor)+str(Faixas[4].valor)+'E'+str(Faixas[5].valor)))))
    return 'Erro em conversao de Faixas'

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
