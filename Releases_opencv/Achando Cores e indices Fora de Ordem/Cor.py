import numpy as np
#Definindo classes de cores dos resistores
class Pico(object):
    def __init__(self,inicio,fim,pto_alto):
        self.inicio = inicio
        self.fim = fim
        self.largura = fim-inicio
        self.pto_alto = pto_alto

class Filtro(object):
    def __init__(self,lower,upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)

class Cor(object):
    def __init__(self, valor, nome,color):
        self.valor = valor
        self.color= color
        self.nome = nome
        self.Filtros = []
        self.Picos = []
        self.mask_cnt=0
        self.mask_percent=0
    def add_filtro(self,lower,upper):
        self.Filtros.append(Filtro(lower,upper))
