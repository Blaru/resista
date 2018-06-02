import matplotlib.pyplot as plt

def plot_Histograma(h,Cores,Filtrado=False,Todos_Filtrados=False,):
    # create some data to use for the plot

    for cor in Cores:
        if(Todos_Filtrados):
            plt.plot(cor.Todas_Cores_Filtradas,color=cor.color)
            plt.axis([-1, len(cor.histograma_Filtrado)+1,0,h])
        elif Filtrado:
            plt.plot(cor.histograma_Filtrado,color=cor.color)
            plt.axis([-1, len(cor.histograma_Filtrado)+1,0,h])
        else:
            plt.plot(cor.histograma,color=cor.color)
            plt.plot(cor.mediana,color=cor.color)
            plt.axis([-1, len(cor.histograma)+1,0,h])
    plt.grid(True)
