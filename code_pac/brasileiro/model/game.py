'''
Created on 05/07/2015

@author: mangeli
'''
from collections import namedtuple
import os
import ConfigParser
import json
from code_pac.configReader import ConfigReader
from code_pac.desafio.aux_old.modelo_old import Player

ItemBRTuple = namedtuple("ItemBRTuple", ['player', 'totalScore'])

class Game:
    def __init__(self, year, gameRounds):
        self.year = year
        self.gameRounds = gameRounds
        

    @classmethod
    def retrieveList(cls):
        games = []
        for gameFile in ConfigReader().listBrasileiroGames():
            f = open(gameFile, 'r')
            j = json.load(f) #a list of rounds
            preGame =[]
            year = gameFile[-4:]
            for r in j:
                gameRound = []
                for p in r:
                    gameRound.append(ItemBRTuple(player=p[0], totalScore=p[1]))
                preGame.append(gameRound)
            games.append(cls(year, preGame))
        return sorted(games, key=lambda g: g.year)
            
            
if __name__ == '__main__':
    print Game.retrieveList()[1].year
    