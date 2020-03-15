'''
Created on 20/06/2015

@author: mangeli
'''


import matplotlib.pyplot as plt
import numpy as np

def plotHistory(p1, p2, order):
    if not len(p1) == len(p2):
        raise Exception('os tamanhos dos arrays p1 e p2 devem ser iguais')
    x=range(len(p1))
    #y=xrange(4)
    fig = plt.figure(order)
    plt.plot(x,p1, '-bo', markersize=8)
    plt.plot(x,p2, '--rD', lw=1.5)
    #plt.yticks([1,2])
    #myYTicks = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    myYTicks = np.arange(0,1.1,0.1)
    plt.yticks(myYTicks)
    plt.ylim(0,1)
    plt.xticks(x)
    plt.vlines(x,0,1, colors='0.75')
    plt.hlines(myYTicks,0,len(p1)-1, colors='0.75')
    #plt.gca().invert_yaxis()
    plt.ylabel("score")
    plt.xlabel('turn')
    return fig

if __name__ == '__main__':
    p1 = [0, 0.1,  0.2, 0.2, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    p2 = [0, 0.05, 0.1, 0.3, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    plot1 = plotHistory(p1, p2, 1)
    
    
    
    p1 = [0, 0.1,  0.2, 0.2, 0.4, 0.5, 0.5, 0.6, 0.7, 0.9, 1]
    p2 = [0, 0.05, 0.1, 0.3, 0.3, 0.4, 0.6, 0.7, 0.8, 0.8, 0.9]
    plot2 = plotHistory(p1, p2, 2)
    
    
    plt.show()