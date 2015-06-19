# -*- coding: utf-8 -*-
'''
Created on 24/05/2015

@author: mangeli
'''
import matplotlib.pyplot as plt
import code_pac.model as model
import numpy as np


class GamePlots(object):
    ''' Game history plots by points and position'''
    def __init__(self, game):
        if not isinstance(game, model.GenericGame):
            raise TypeError("Arg isn't a GenericGame object")
        self._players = game.getPlayers()
        self._gameObj = game.getGameStruct()
        
        
    def byPoints(self):
        x = xrange(1, len(self._gameObj)+1)
        #plt.subplot(2,1,1)
        plt.figure()
        for player in self._players:
            y=[]
            for i in range(0, len(self._gameObj)):
                found = False
                for result in self._gameObj[i][1]:
                    if result.playerCode == player:
                        found = True
                        y.append(result.totalScore)
                if not found:
                    y.append(float(0))
            plt.plot(x,y,'o-',linewidth=2)
        plt.ylabel(u'pontuação')
        plt.xlabel(u'rodada')    
        plt.show()
        
    def byPosition(self):
        #plt.subplot(2,1,2)
        x = xrange(1, len(self._gameObj)+1)
        x = np.array(x)
        for player in self._players:
            y=[]
            for i in range(0, len(self._gameObj)):
                if i == 0: #every one starts in same position
                    #y.append(len(jogadores))
                    y.append(1)
                    pass
                else:
                    found = False
                    for result in self._gameObj[i][1]:
                        if result.playerCode == player:
                            found = True
                            y.append(self._gameObj[i][1].index(result) + 1)
                    if not found:
                        y.append(len(self._players))
            y = np.array(y)
            plt.plot(x,y,'o-',linewidth=2)
        #plt.ylim(0, len(self._players)+1)
        plt.yticks(xrange(0,len(self._players)+1))
        plt.ylabel(u'posição')
        plt.xlabel(u'rodada')
        plt.gca().invert_yaxis()    
        plt.show()