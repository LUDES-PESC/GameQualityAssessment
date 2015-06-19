'''
Created on 15/06/2015

@author: mangeli
'''
import matplotlib
import numpy as np
from code_pac.model import DesafioGame

def position(inputGame, panel):
    obj = DesafioGame(inputGame)
    players = obj.getPlayers()
    gameObj = obj.getGameStruct()
    panel.figure.clf()
    axes = panel.figure.gca()    
    
    x = xrange(1, len(gameObj)+1)
    x = np.array(x)
    for player in players:
        y=[]
        for i in range(0, len(gameObj)):
            if i == 0: #every one starts in same position
                #y.append(len(jogadores))
                y.append(1)
                pass
            else:
                found = False
                for result in gameObj[i][1]:
                    if result.playerCode == player:
                        found = True
                        y.append(gameObj[i][1].index(result) + 1)
                if not found:
                    y.append(len(players))
        y = np.array(y)
        axes.plot(x,y,'o-',linewidth=2)
    #plt.ylim(0, len(self._players)+1)
    axes.set_yticks(xrange(0,len(players)+1))
    axes.set_ylabel('Position')
    axes.set_xlabel('Turn')
    axes.invert_yaxis()    
    panel.draw()
    
def points(inputGame, panel):
    obj = DesafioGame(inputGame)
    players = obj.getPlayers()
    gameObj = obj.getGameStruct()
    panel.figure.clf()
    axes = panel.figure.gca()
    
    x = xrange(1, len(gameObj)+1)
    for player in players:
        y=[]
        for i in range(0, len(gameObj)):
            found = False
            for result in gameObj[i][1]:
                if result.playerCode == player:
                    found = True
                    y.append(result.totalScore)
            if not found:
                y.append(float(0))
        axes.plot(x,y,'o-',linewidth=2)
    
    axes.set_ylabel('Points')
    axes.set_xlabel('Turn')
    panel.draw()
    
def histGeral(values, panel, xLabel=''):
    panel.figure.clf()
    axes = panel.figure.gca()
    axes.hist(values)
    axes.set_xlabel(xLabel)
    panel.draw()
      