import matplotlib.pyplot as plt
import numpy as np



"""
def demo(sty):
    mpl.style.use(sty)
    fig, ax = plt.subplots(figsize=(3, 3))

    ax.set_title('style: {!r}'.format(sty), color='C0')

    ax.plot(th, np.cos(th), 'C1', label='C1')
    ax.plot(th, np.sin(th), 'C2', label='C2')
    ax.legend()
    #"""

def plot_Histograma(plt,h,w,Cores):
    # create some data to use for the plot

    for cor in Cores:
        plt.plot(cor.histograma,color=cor.color)
        plt.plot(cor.mediana,color=cor.color)
    plt.xlabel('pixels[px]')
    plt.ylabel('densidade[px]')
    plt.axis([-1, w/2+1,0,h])
    plt.grid(True)
