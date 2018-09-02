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

from collections import namedtuple

        
def plotaHistogramaDramaPorPontos(dramas):
    plot.hist(dramas, bins=100)
    plot.ylabel('Frequência de Simulações');
    plot.xlabel('Drama por Pontos');
    plot.title('Distribuição da Métrica de Drama por Pontos')
    plot.show()
    plot.savefig('dramapontos_grupo3.png')
    
    
def plotaHistogramaDramaPorPosicao(dramas):
    plot.hist(dramas, bins=50)
    plot.ylabel('Frequência de Simulações');
    plot.xlabel('Drama por Posição');
    plot.title('Distribuição da Métrica de Drama por Posição')
    plot.show()
    plot.savefig('dramaposicao_grupo3.png')
    
    
def plotaHistogramaDramaPorCaminho(dramas):
    plot.hist(dramas, bins=50)
    plot.ylabel('Frequência de Simulações');
    plot.xlabel('Drama por Caminho');
    plot.title('Distribuição da Métrica de Drama por Caminho')
    plot.show()
    plot.savefig('dramacaminho_grupo3.png')
    
    
if __name__ == '__main__':

    dramasPontos = [];
    dramasPosicao = [];
    dramasCaminho = [];
    with open("dramaporpontos_grupo4.txt", "r") as arquivo:
        for linha in arquivo:
            if(float(linha) != 0 ):
                dramasPontos.append(float(linha))
    print "Drama por Pontos"
    print "Quantidade de Dramas"
    print len(dramasPontos)
    
    print "Media"
    print np.mean(dramasPontos)
    
    print "Desvio Padrão"
    print np.std(dramasPontos)
   
    plotaHistogramaDramaPorPontos(dramasPontos)
    
    
    
    with open("dramaporposicao_grupo4.txt", "r") as arquivo:
        for linha in arquivo:
            if(float(linha) != 0 ):
                dramasPosicao.append(float(linha))
    
    print "Drama por Posicao"
    print "Quantidade de Dramas"
    print len(dramasPosicao)
    
    print "Media"
    print np.mean(dramasPosicao)
    
    print "Desvio Padrão"
    print np.std(dramasPosicao)
   
    plotaHistogramaDramaPorPosicao(dramasPosicao)
    
    
    
    with open("dramaporcaminho_grupo4.txt", "r") as arquivo:
        for linha in arquivo:
            if(float(linha) != 0 ):
                dramasCaminho.append(float(linha))
                
                
    print "Drama por Caminho"
    print "Quantidade de Dramas"
    print len(dramasCaminho)
    
    print "Media"
    print np.mean(dramasCaminho)
    
    print "Desvio Padrão"
    print np.std(dramasCaminho)
   
    plotaHistogramaDramaPorCaminho(dramasCaminho)
    