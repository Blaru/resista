from Cor import Cor
#________________________________________________
Preto = Cor(0,"Preto")
Preto.add_filtro([16, 0, 0],[30, 163, 165])

#________________________________________________
Marrom = Cor(1,"Marrom")
Marrom.add_filtro([7, 61, 119],[12, 127, 210])
Marrom.add_filtro([4, 61, 119],[7, 127, 210])

#________________________________________________
Vermelho=	Cor(2,"Vermelho")
Vermelho.add_filtro([0, 76, 45],[7, 255, 2555])
Vermelho.add_filtro([170, 65, 102],[180, 255, 255])

#________________________________________________
Laranja = Cor(3,"Laranja")
Laranja.add_filtro([10, 81, 178],[13, 164, 238])

#________________________________________________
Amarelo	=	Cor(4,"Amarelo")
Amarelo.add_filtro([20, 130, 100],[30, 250, 160])

#________________________________________________
Verde	=	Cor(5,"Verde")
Verde.add_filtro([45, 50, 60],[72, 250, 150])

#________________________________________________
Azul	=	Cor(6,"Azul")
Azul.add_filtro([80, 50, 50],[106, 250, 150])

#________________________________________________
Roxo	=	Cor(7,"Roxo")
Roxo.add_filtro([130, 40, 50],[155, 250, 150])

#________________________________________________
Cinza	=	Cor(8,"Cinza")
Cinza.add_filtro([0,0, 50],[180, 50, 80])

#________________________________________________
Branco	=	Cor(9,"Branco")
Branco.add_filtro([0, 0, 90],[180, 15, 140])

#________________________________________________
Cores=[]
Cores.append(Preto)
Cores.append(Marrom)
Cores.append(Vermelho)
Cores.append(Laranja)
Cores.append(Amarelo)
Cores.append(Verde)
Cores.append(Azul)
Cores.append(Roxo)
Cores.append(Cinza)
Cores.append(Branco)