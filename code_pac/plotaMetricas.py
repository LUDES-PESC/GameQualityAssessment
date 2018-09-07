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

        
def plotaHistograma(valores, nomeMetrica, ymax, nbins, variante):
    plot.hist(valores, bins=nbins)
    plot.ylabel('Frequência de Simulações');
    if(ymax != 0):
        plot.ylim=(ymax)
    else:
        plot.autoscale(True)
    plot.xlabel(nomeMetrica);
    plot.title('Distribuição da Métrica de ' + nomeMetrica + ' ' + variante)
    
    plot.savefig('Distribuição da Métrica de ' + nomeMetrica + ' ' + variante+ '.png')
    plot.show()


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
    
    indiceVariante = "1";
    variante = "5 Rodadas"
    
    
    
    
    dramasPontos = leArquivo("dramaporpontos_grupo"+ indiceVariante +".txt");
    salvarDados("Drama por Pontos", dramasPontos, indiceVariante);
    plotaHistograma(dramasPontos, "Drama por Pontos", 0, 100, variante);
    
    dramasPosicao = leArquivo("dramaporposicao_grupo"+ indiceVariante +".txt");
    salvarDados("Drama por Posicao", dramasPosicao, indiceVariante);    
    plotaHistograma(dramasPosicao, "Drama por Posição", 0, 50, variante)
    
    dramasCaminho = leArquivo("dramaporcaminho_grupo"+ indiceVariante +".txt");
    salvarDados("Drama por Caminho", dramasCaminho, indiceVariante);
    plotaHistograma(dramasCaminho, "Drama por Caminho", 1000, 50, variante)
    
    leadChange = leArquivo("leadchange_grupo"+ indiceVariante +".txt");
    salvarDados("Mudanca de Lideranca", leadChange, indiceVariante);
    plotaHistograma(leadChange, "Mudança de Liderança", 0, 20, variante) 
    
    incertezaEntropia = leArquivo("incertezaentropia_grupo"+ indiceVariante +".txt");
    salvarDados("Incerteza por Entropia", incertezaEntropia, indiceVariante);
    plotaHistograma(incertezaEntropia, "Incerteza por Entropia", 0, 100, variante)
    
    incertezaPDD = leArquivo("incertezapdd_grupo"+ indiceVariante +".txt");
    salvarDados("Incerteza por PDD", incertezaPDD, indiceVariante);
    plotaHistograma(incertezaPDD, "Incerteza por PDD", 0 , 100, variante)