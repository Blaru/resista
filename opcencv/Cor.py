import numpy as np
#Definindo classes de cores dos resistores
class Cor(object):
    def __init__(self, valor, nome, lower, upper):
        self.valor = valor
        self.nome = nome
        self.lower = np.array(lower)
        self.upper = np.array(upper)
