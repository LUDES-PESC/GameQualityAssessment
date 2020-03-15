# -*- coding: utf-8 -*-
'''
Created on 14/07/2015

@author: Augusto
'''
from __future__ import unicode_literals
from GameQualityAssessment.code_pac import dataBaseAdapter
from GameQualityAssessment.code_pac.gamePlots import GamePlots
import GameQualityAssessment.code_pac.model as model
from GameQualityAssessment.code_pac.measures import DramaByPaths, DramaByPointsUp2First, DramaByPositionUp2First
import GameQualityAssessment.code_pac.diceGame.model as diceGameModel
from GameQualityAssessment.project_path import make_absolute_path as abspath
import matplotlib.pyplot as plot
import numpy as np
import scipy.stats as stats
from scipy.interpolate import UnivariateSpline
from numpy import linspace
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter
from collections import namedtuple

        
def plotaHistograma(valores, nomeMetrica, ymax, nbins, variante):
    density = stats.gaussian_kde(valores)
    

def leArquivo(caminho):
    listaValores = []
    with open(caminho, "r") as arquivo:
        for linha in arquivo:
            if(float(linha) != 0 ):
                listaValores.append(float(linha))
    return listaValores
    
def salvarDados( metrica , listaValores, indiceVariante):
    with open(abspath("dados_grupo"+ indiceVariante +".txt"), 'a') as fp:
        fp.write('{} {} {} {}\n'.format(metrica, len(listaValores), np.mean(listaValores), np.std(listaValores)))
    
def plot_dimension(array_embedding, array_day):
    listaValores = []
    
    
if __name__ == '__main__':
    mediaDramaPontos = [0.3766 , 0.3832 , 0.3221 , 0.2886 , 0.3006 , 0.2436 , 0.3096]
    mediaDramaPosicao = [0.5888 , 0.5892 , 0.5919 , 0.5932 , 0.5954 , 0.5942 , 0.5938]
    mediaDramaCaminho = [0.2343 , 0.2365 , 0.2397 , 0.2486 , 0.2521 , 0.2487 , 0.2508]
    variantes = ["10Rd6", "10Rd10", "10R2d5", "50Rd6" , "50Rd10", "50R2d5", "50Rd50"]
    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(mediaDramaPontos, mediaDramaPosicao, mediaDramaCaminho)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    ax.set_xlabel('Drama por Pontos')
    ax.set_ylabel('Drama por Posicao')
    ax.set_zlabel('Drama por Caminho')
    plot.show()
    