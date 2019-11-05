# -*- coding: utf-8 -*-
'''
Created on 14/07/2015

@author: Augusto
'''
from __future__ import unicode_literals
from GameQualityAssessment.code_pac import dataBaseAdapter
from GameQualityAssessment.code_pac.gamePlots import GamePlots
import GameQualityAssessment.code_pac.model as model
from GameQualityAssessment.code_pac.measures import DramaByPaths, DramaByPointsUp2First, DramaByPositionUp2First, LeadChange, UncertaintyEntropy, UncertaintyPDD
import GameQualityAssessment.code_pac.diceGame.model as diceGameModel
from GameQualityAssessment.project_path import make_absolute_path as abspath
import matplotlib.pyplot as plot

from collections import namedtuple

def calculaDramaPorPontos(game):
    obj = model.DiceGame(game)
    value = DramaByPointsUp2First(game=obj, ignored=0)
    return value.getMeasureValue()    
    
def calculaDramaPorCaminho(game):
    obj = model.DiceGame(game)
    value = DramaByPaths(game=obj, ignored=0)
    return value.getMeasureValue()  

def calculaDramaPorPosicao(game):
    obj = model.DiceGame(game)
    value = DramaByPositionUp2First(game=obj, ignored=0)
    return value.getMeasureValue()  

def calculaMudancasLideranca(game):
    obj = model.DiceGame(game)
    value = LeadChange(game=obj, ignored=0)
    return value.getMeasureValue()  

def calculaIncertezaEntropia(game):
    obj = model.DiceGame(game)
    value = UncertaintyEntropy(game=obj, ignored=0)
    return value.getMeasureValue()  

def calculaIncertezaPDD(game):
    obj = model.DiceGame(game)
    value = UncertaintyPDD(game=obj, ignored=0)
    return value.getMeasureValue()  

    
def plotaGraficoPorPontos(game):
    obj = model.DiceGame(game)
    GamePlots(obj).byPoints()

def plotaGraficoPorPosicao(game):
    obj = model.DiceGame(game)
    GamePlots(obj).byPosition()    

def winnerPosition(x):
    return {
        'p0': 0,
        'p1': 1,
        'p2': 2,
        'p3': 3
    }[x]

def plotaPieChart(numberWins):
    labels = 'Player 1', 'Player 2', 'Player 3', 'Player 4'
    explode = (0, 0, 0, 0)
    fig1, ax1 = plot.subplots()
    ax1.pie(numberWins, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plot.show()
    
def winnerPieChart(games):
    players = model.DiceGame(games[0]).getPlayers()
    numberPlayers = len(players)
    numberWins = []
    for i in range(numberPlayers):
        numberWins.append(0)
    for game in games:
        obj = model.DiceGame(game)
        winner = obj.getWinner()
        numberWins[winnerPosition(winner)] = numberWins[winnerPosition(winner)] + 1        
    print (numberWins)
    plotaPieChart(numberWins)
        

def salvaArquivoValores(valores, arquivo):
    with open(arquivo, 'w') as f:
        for valor in valores:
            f.write("%s\n" % valor)   

def calculaESalvaDramas(games, indiceVariante):
    dramasPontos = []
    dramasPosicao = []
    dramasCaminho = []
    for game in games:
        dramasPontos.append(calculaDramaPorPontos(game))
        dramasPosicao.append(calculaDramaPorPosicao(game))
        dramasCaminho.append(calculaDramaPorCaminho(game))
        
    salvaArquivoValores(dramasPontos, abspath('code_pac/dramaporpontos_grupo'+ indiceVariante +'.txt'))
    salvaArquivoValores(dramasPosicao, abspath('code_pac/dramaporposicao_grupo'+ indiceVariante +'.txt'))
    salvaArquivoValores(dramasCaminho, abspath('code_pac/dramaporcaminho_grupo'+ indiceVariante +'.txt'))

def calculaESalvaMudancaLideranca(games, indiceVariante):
    mudancaLiderancao = []
    for game in games:
        mudancaLiderancao.append(calculaMudancasLideranca(game))
    salvaArquivoValores(mudancaLiderancao, abspath('code_pac/deadchange_grupo'+ indiceVariante +'.txt'))
    
    
def calculaESalvaIncerteza(games, indiceVariante):
    incertezaEntropia = []
    incertezaPDD = []
    for game in games:
        incertezaEntropia.append(calculaIncertezaEntropia(game))
        incertezaPDD.append(calculaIncertezaPDD(game))
    salvaArquivoValores(incertezaEntropia, abspath('code_pac/dncertezaentropia_grupo'+ indiceVariante +'.txt'))
    salvaArquivoValores(incertezaPDD, abspath('code_pac/dncertezapdd_grupo'+ indiceVariante +'.txt'))


if __name__ == '__main__':
    
    games = diceGameModel.Game.retrieveList()
    
    #for game in games:
    #    print calculaIncertezaPDD(game);
    
    #winnerPieChart(games)
    #quebrando para nao rodar sem querer
    indiceVariante = "2"
    calculaESalvaDramas(games, indiceVariante)
    calculaESalvaMudancaLideranca(games, indiceVariante)
    calculaESalvaIncerteza(games, indiceVariante)
    #print calculaDramaPorPontos(games[0]);
    #print calculaDramaPorCaminho(games[0]);
    #print calculaDramaPorPosicao(games[0]);
    #plotaGraficoPorPontos(games[0]);
    #plotaGraficoPorPosicao(games[0])
    #winnerPieChart(games)
    #for game in games:
        #obj = model.DiceGame(game)
        #print obj.getWinner();
        
        
    
   

    #print value.getWinner(), value.getMeasureValue()
    #print value.getType().description
    
    
    

    
    