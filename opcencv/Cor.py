import numpy as np
#Definindo classes de cores dos resistores

class Filtro(object):
    def __init__(self,lower,upper):
        self.lower = np.array(lower)
        self.upper = np.array(upper)

class Cor(object):
    def __init__(self, valor, nome):
        self.valor = valor
        self.nome = nome
        self.Filtros = []
        self.mask_cnt=0
        self.mask_percent=0
    def add_filtro(self,lower,upper):
        self.Filtros.append(Filtro(lower,upper))
