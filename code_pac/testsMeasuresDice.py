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
    
def plotaGraficoPorPontos(game):
    obj = model.DiceGame(game);
    GamePlots(obj).byPoints();

def plotaGraficoPorPosicao(game):
    obj = model.DiceGame(game);
    GamePlots(obj).byPosition();    

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
    fig1, ax1 = plot.subplots();
    ax1.pie(numberWins, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plot.show()
    
def winnerPieChart(games):
    players = model.DiceGame(games[0]).getPlayers()
    numberPlayers = len(players);
    numberWins = [];
    for i in range(numberPlayers):
        numberWins.append(0);
    for game in games:
        obj = model.DiceGame(game);
        winner = obj.getWinner();
        numberWins[winnerPosition(winner)] = numberWins[winnerPosition(winner)] + 1        
    print numberWins;
    plotaPieChart(numberWins)
        
def plotaHistogramaDramaPorPontos(dramas):
    plot.hist(dramas, bins=30)
    plot.ylabel('Frequência de Simulações');
    plot.xlabel('Drama por Pontos');
    plot.title('Distribuição da Métrica de Drama por Pontos')
    plot.show()


def salvaArquivoDrama(dramas, arquivo):
    with open(arquivo, 'w') as f:
        for drama in dramas:
            f.write("%s\n" % drama)   

def calculaESalvaDramas(games):
    dramasPontos = [];
    dramasPosicao = [];
    dramasCaminho = [];
    for game in games:
        dramasPontos.append(calculaDramaPorPontos(game))
        dramasPosicao.append(calculaDramaPorPosicao(game))
        dramasCaminho.append(calculaDramaPorCaminho(game))
        
    salvaArquivoDrama(dramasPontos, 'dramaporpontos_grupo5.txt')
    salvaArquivoDrama(dramasPosicao, 'dramaporposicao_grupo5.txt')
    salvaArquivoDrama(dramasCaminho, 'dramaporcaminho_grupo5.txt')
            
if __name__ == '__main__':
    games = diceGameModel.Game.retrieveList();
    
    #winnerPieChart(games)
    
    calculaESalvaDramas(games);

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
    
    
    

    
    