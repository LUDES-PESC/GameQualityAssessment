# -*- coding: utf-8 -*-
'''
Created on 14/07/2015

@author: Augusto
'''
from __future__ import unicode_literals
from code_pac import dataBaseAdapter
from code_pac.gamePlots import GamePlots
import code_pac.model as model
from code_pac.measures import DramaByPaths, DramaByPointsUp2First, DramaByPositionUp2First
import code_pac.diceGame.model as diceGameModel
import matplotlib.pyplot as plot
import numpy as np
import scipy.stats as stats
from scipy.interpolate import UnivariateSpline
from numpy import linspace

from collections import namedtuple

        
def plotaHistograma(valores, nomeMetrica, ymax, nbins, variante):
    #density = stats.gaussian_kde(valores)
    #plot.hist(valores, bins=nbins, histtype = 'step', normed=True)
    #plot.plot(x, density(x))
    
    
    
    kde = stats.gaussian_kde( valores )
    dist_space = linspace( min(valores), max(valores), 100 )
    
    ax.plot( dist_space, kde(dist_space) , label= variante)
    
    #if(ymax != 0):
    #    plot.ylim=(ymax)
    #else:
    #    plot.autoscale(True)

   
    
    #plot.savefig('Distribuição da Métrica de ' + nomeMetrica + ' ' + variante+ '.png')
    #plot.show()


def leArquivo(caminho):
    listaValores = []
    with open(caminho, "r") as arquivo:
        for linha in arquivo:
            if(float(linha) != 0 ):
                listaValores.append(float(linha))
    return listaValores;
    
def salvarDados( metrica , listaValores, indiceVariante):
    with open("dados_grupo"+ indiceVariante +".txt", 'a') as fp:
        fp.write('{} {} {} {}\n'.format(metrica, len(listaValores), np.mean(listaValores), np.std(listaValores)))
    
if __name__ == '__main__':
    
    #1 - 10Rd6
    #2 - 10Rd10
    #3 - 50R2d5
    #4 - 50Rd10
    #5 - 10R2d5
    #6 - 50Rd6
    #7 - 50Rd50
    variantes = ["10Rd6", "10Rd10", "50R2d5", "50Rd10" , "10R2d5" , "50Rd6" , "50Rd50"]
    indiceVariante = "1";    
    nomeMetrica =  "Drama por Caminho"
    plot.figure();
    ax = plot.subplot(111)
    plot.ylabel('Frequência de Simulações');
    plot.title('Distribuição do ' + nomeMetrica + ' nas variantes do DicePoints')
    plot.xlabel(nomeMetrica);
    
    for indiceVariante in range(7):
        dramasPontos = leArquivo("dramaporcaminho_grupo"+ str(indiceVariante+1) +".txt");
        print indiceVariante;
        #salvarDados("Drama por Pontos", dramasPontos, indiceVariante);
        plotaHistograma(dramasPontos, nomeMetrica, 0, 50, variantes[indiceVariante]);
    ax.legend()
    plot.savefig('dist_dramaporcaminho.png')
    plot.show()
    