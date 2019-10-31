# -*- coding: utf-8 -*-
'''
Created on 24/05/2015

@author: mangeli
'''
#from code_pac.model import GenericGame
from collections import namedtuple

MeasureType = namedtuple("MeasureType", ["code", "description", "version"])

class MeasureTemplate(object):
    '''Template for drama measure implementations'''
    
    _measureType = ''
    _measureValue = ''

    def __init__(self, *args, **kwargs):
        '''if not isinstance(game, GenericGame):
            raise TypeError("Arg isn't a GenericGame object") '''
        
        #some games have first rounds without results
        if kwargs.get('ignored') == None:
            self._ignored = 0 
        else:
            self._ignored = kwargs.get('ignored')
        
        #some games have variable high scores for each round and the
        #higher game score doesn't mean the game ending
        #so we don't normalize scores
        if kwargs.get('normScores') == None:
            self._normScores = False
        else:
            self._normScores = kwargs.get('normScores')
            
        #some games have a minumum number of points other than 0
        if kwargs.get('minScore') == None:
            self._minScore = 0
        else:
            self._minScore = kwargs.get('minScore')
            
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
        return self._measureValue
    
    def getWinner(self):
        return self._winner
    
    def getType(self):
        if not isinstance(self._measureType, MeasureType):
            raise TypeError('Measure type has a wrong definition')
        return self._measureType

