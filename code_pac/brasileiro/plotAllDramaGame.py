# -*- coding: utf-8 -*-
'''
Created on 20/07/2015

@author: mangeli
'''
from __future__ import division
from code_pac.brasileiro.model.game import Game
from code_pac.model import BrasileiroGame
import matplotlib.pyplot as plt
import numpy as np
import math
from code_pac.measures import DramaByPaths, DramaByPositionUp2First, DramaByPointsUp2First

def maxDrama(nPlayers, nRounds, m):
        x1 = 1 #primeira rodada 
        y1 = nPlayers #na última posição
        x2 = nRounds #última rodada
        y2 = 1 #primeira posição
        return math.ceil((y2-y1)*(m-x1)/(x2-x1) + y1 )

def plotPath(players, rounds, order, winnerPath, dValues):
    
    x=xrange(1, rounds+1)
    y=[]
    for res in x:
        y.append(maxDrama(players, rounds,res))
    #y=xrange(4)
    fig = plt.figure(order)
    
    #plt.plot(x,y, '-mo', markersize=8, clip_on=False, label="MDP") #MDP
    plt.plot(x,winnerPath, '-bs', markersize=8, clip_on=False, label="Winner Path")
        
    plt.yticks(xrange(1,players+1))
    plt.xticks(np.arange(1,rounds+1,3))
    
    plt.gca().invert_yaxis()
    
    plt.title(order)
    plt.vlines(x,1,players, colors='0.75')
    plt.hlines(xrange(1,players),1,rounds, colors='0.75')
    plt.ylabel("position")
    plt.xlabel('turn')
    fString = '{0:.4f}'
    '''plt.gca().text(0.63,0.02,'Drama by Path: ' + fString.format(dValues[0]) + '\n'
                   + 'Drama by Points: ' + fString.format(dValues[1]) + '\n'
                   + 'Drama by Position: ' + fString.format(dValues[2])
                   ,transform=plt.gca().transAxes,
                   verticalalignment='bottom', horizontalalignment='left', backgroundcolor='white')
    '''
    plt.legend(fontsize='medium', loc=7)
    return fig

if __name__ == '__main__':
    games = Game.retrieveList()
    anos = xrange(2003, 2015);
    #ano = '2013'
    game = None
    contador = 1;
    for ano in anos:
        for g in games:
            if g.year == str(ano):
                game = g
                break
        
        genGame = BrasileiroGame(game)
        winner = genGame.getWinner()
        nPlayers = len(genGame.getPlayers())
        nRounds = genGame.getNumberRounds()
        winnerPath = []
        for i in xrange(1, nRounds + 1):
            gameRound = genGame.getRound(i)[1]
            for r in gameRound:
                if r.playerCode == winner:
                    winnerPath.append(gameRound.index(r)+1)
                    break
        dramaPath = DramaByPaths(game=genGame, ignored=0).getMeasureValue() 
        dramaPoints = DramaByPointsUp2First(game=genGame, ignored=0, normScores=True).getMeasureValue()
        dramaPosition = DramaByPositionUp2First(game=genGame, ignored=0).getMeasureValue()
        dValues = (dramaPath, dramaPoints, dramaPosition)
        
        plotPath(nPlayers, nRounds, contador, winnerPath, dValues)
        contador += 1
    plt.show()