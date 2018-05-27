import matplotlib.pyplot as plt
import numpy as np

def plot_Histograma(plt,h,w,Cores):
    # create some data to use for the plot

    for cor in Cores:
        plt.plot(cor.histograma,color=cor.color)
        plt.plot(cor.mediana,color=cor.color)
    plt.xlabel('pixels[px]')
    plt.ylabel('densidade[px]')
    plt.axis([-1, w/2+1,0,h])
    plt.grid(True)
