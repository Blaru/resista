import matplotlib.pyplot as plt

def plot_Histograma(plt,h,w,Cores,Filtrado=False):
    # create some data to use for the plot
    for cor in Cores:
        if Filtrado:
            plt.plot(cor.histograma_Filtrado,color=cor.color)
        else:
            plt.plot(cor.histograma,color=cor.color)
        plt.plot(cor.mediana,color=cor.color)
    plt.xlabel('pixels[px]')
    plt.ylabel('densidade[px]')
    plt.axis([-1, w/2+1,0,h])
    plt.grid(True)
