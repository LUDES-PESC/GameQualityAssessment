# -*- coding: utf-8 -*-
'''
Created on 24/05/2015

@author: mangeli
'''
from code_pac.model import GenericGame
from collections import namedtuple

MeasureType = namedtuple("MeasureType", ["code", "description", "version"])

class MeasureTemplate(object):
    '''Template for drama measure implementations'''
    
    def __init__(self, *args, **kwargs):
        '''if not isinstance(game, GenericGame):
            raise TypeError("Arg isn't a GenericGame object") '''
        
        #some games has first rounds without results
        if kwargs.get('ignored') == None:
            self._ignored = 0 
        else:
            self._ignored = kwargs.get('ignored')
        
        #some games has variable high scores round bases so the
        #higher game score doesn't mean the game ending
        if kwargs.get('normScores') == None:
            self._normScores = False
        else:
            self._normScores = kwargs.get('normScores')
        
        self._game = kwargs.get('game')
        self._findWinner()
        self._evaluateMeasure()
        
    
    def _findWinner(self):
        self._winner = self._game.getWinner()
    
    def setIgnored(self, ig):
        self._ignored = ig
        return self
        
    def getIgnored(self, ig):
        return self._ignored
    
    def _evaluateMeasure(self):
        raise NotImplementedError()
    
    def getMeasureValue(self):
        return self._drama
    
    def getWinner(self):
        return self._winner
    
    def getType(self):
        if not isinstance(self._measureType, MeasureType):
            raise TypeError('Measure type has a wrong definition')
        return self._measureType

