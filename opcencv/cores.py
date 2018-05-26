from Cor import Cor
#________________________________________________
Preto = Cor(0,"Preto",'black')
Preto.add_filtro([15, 51, 0],[30, 102, 90])

#________________________________________________
Marrom = Cor(1,"Marrom",'brown')
#Marrom.add_filtro([5, 56, 17],[16, 178, 102])  #Marrom 4
Marrom.add_filtro([5, 56, 17],[16, 178, 91])  #Marrom 4.2
Marrom.add_filtro([0, 117, 53],[12, 229, 115])  #Marrom 5
Marrom.add_filtro([177, 117, 53],[180, 229, 115])  #Marrom 5
Marrom.add_filtro([8, 61, 120],[12, 130, 170])  #Marrom 6
#Marrom.add_filtro([4, 61, 119],[7, 127, 210])

#________________________________________________
Vermelho=	Cor(2,"Vermelho",'red')
Vermelho.add_filtro([2, 216, 56],[9, 255, 107])         #Vermelho 1
Vermelho.add_filtro([1, 183, 102],[3, 255, 192])        #Vermelho 2
Vermelho.add_filtro([178, 183, 102],[180, 255, 192])    #Vermelho 2
Vermelho.add_filtro([3, 150, 46],[10, 255, 104])    #Vermelho 3

#________________________________________________
Laranja = Cor(3,"Laranja",'orange')
Laranja.add_filtro([22, 72, 74],[26, 104, 90])     #Laranja 1
Laranja.add_filtro([12, 150, 69],[15, 255, 107])    #Laranja 2
Laranja.add_filtro([9, 143, 62],[12, 255, 125])     #Laranja 3
Laranja.add_filtro([8, 71, 176],[14, 158, 244])     #Laranja 4

#________________________________________________
Amarelo	=	Cor(4,"Amarelo",'yellow')
Amarelo.add_filtro([19, 125, 91],[25, 250, 120]) #Todos os Amarelos

#________________________________________________
Verde	=	Cor(5,"Verde",'lime')
Verde.add_filtro([45, 130, 58],[72, 255, 150])  # Verde 1

#________________________________________________
Azul	=	Cor(6,"Azul",'blue')
Azul.add_filtro([80, 50, 50],[106, 250, 150])   #

#________________________________________________
Roxo	=	Cor(7,"Roxo",'purple')
Roxo.add_filtro([0, 46, 28],[2, 220, 188])
Roxo.add_filtro([140, 46, 28],[180, 220, 188])

#________________________________________________
Cinza	=	Cor(8,"Cinza",'grey')
Cinza.add_filtro([0,0, 50],[180, 50, 80])

#________________________________________________
Branco	=	Cor(9,"Branco",'white')
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
