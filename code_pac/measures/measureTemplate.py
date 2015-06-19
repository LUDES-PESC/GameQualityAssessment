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
    
    def __init__(self, game):
        '''if not isinstance(game, GenericGame):
            raise TypeError("Arg isn't a GenericGame object") '''
        self._game = game
        self._findWinner()
        self._evaluateMeasure()
        
    
    def _findWinner(self):
        self._winner = self._game.getWinner()
    
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

