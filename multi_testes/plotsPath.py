# -*- coding: utf-8 -*-
'''
Created on 15/07/2015

@author: mangeli
'''
from __future__ import division
import matplotlib.pyplot as plt
import math

def maxDrama(nPlayers, nRounds, m):
        x1 = 1 #primeira rodada 
        y1 = nPlayers #na última posição
        x2 = nRounds #última rodada
        y2 = 1 #primeira posição
        return math.ceil((y2-y1)*(m-x1)/(x2-x1) + y1 )

def plotPath(players, rounds, order):
    
    x=xrange(1, rounds+1)
    y=[]
    for res in x:
        y.append(maxDrama(players, rounds,res))
    #y=xrange(4)
    fig = plt.figure(order)
    
    plt.plot(x,y, '-mo', markersize=8, clip_on=False)
        
    plt.yticks(xrange(1,players+1))
    plt.xticks(xrange(1,rounds+1))
    
    plt.gca().invert_yaxis()
    
    
    plt.vlines(x,1,players, colors='0.75')
    plt.hlines(y,1,rounds, colors='0.75')
    plt.ylabel("position")
    plt.xlabel('turn')
    return fig

if __name__ == '__main__':
    plot1 = plotPath(10, 10, 1)
    plot2 = plotPath(7, 10, 2)
    plot3 = plotPath(5, 10, 3)
    plt.show()