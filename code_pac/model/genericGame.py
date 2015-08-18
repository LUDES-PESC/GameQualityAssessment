'''
Created on 28/05/2015

@author: mangeli
'''
from collections import namedtuple

ItemTuple = namedtuple("ItemTuple", ['playerCode', 'roundScore', 'totalScore'])

class GenericGame(object):
    '''
    A generic class for games with turns (rounds) and variable number of players
    '''

    def __init__(self, game):
        self._game = game
        self._setGameStruct()
        
    def _setGameStruct(self):
        '''
        roundNumber
           |_ playerCode, roundScore, totalScore
        ''' 
        raise NotImplementedError()
    
    def getGameStruct(self):
        return self._gameData
        
    def getNumberRounds(self):
        return len(self._gameData)
    
    def getRound(self, roundNumber):
        '''starting from 1'''
        return self._gameData[roundNumber - 1]
    
    def getWinner(self):
        return self._gameData[len(self._gameData) -1][1][0][0]
    
    def getLastRound(self):
        return self._gameData[len(self._gameData) - 1]
    
    def getPlayers(self):
        return self._players
    
    