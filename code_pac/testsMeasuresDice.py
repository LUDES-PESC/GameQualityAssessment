# -*- coding: utf-8 -*-
'''
Created on 14/07/2015

@author: mangeli
'''
from code_pac import dataBaseAdapter
from code_pac.gamePlots import GamePlots
import code_pac.model as model
from code_pac.measures import DramaByPaths, DramaByPointsUp2First
import code_pac.diceGame.model as diceGameModel

from collections import namedtuple

   
if __name__ == '__main__':
    game = diceGameModel.Game.retrieveList()[0];
    print game;
    obj = model.DiceGame(game)
    value = DramaByPointsUp2First(game=obj, ignored=0, normScores=True)
    print value.getWinner(), value.getMeasureValue()
    print value.getType().description
    GamePlots(obj).byPoints()
    
    
    
    