'''
Created on 05/07/2015

@author: mangeli
'''
#from collections import namedtuple
import os
import configparser
import json
from GameQualityAssessment.code_pac.configReader import ConfigReader
from GameQualityAssessment.code_pac.desafio.aux_old.modelo_old import Player

#ItemBRTuple = namedtuple("ItemBRTuple", ['player', 'totalScore'])

class Game:
    def __init__(self, year, gameRounds=None):
        self.year = year
        if gameRounds == None:
            self.gameRounds = Game.__getGameRoundsByYear(year)
        else:
            self.gameRounds = gameRounds
    
    @classmethod
    def __getGameRoundsByYear(cls,year):
        foundGameFile = None
        for gameFile in ConfigReader().listLegaNazionaleGames():
            if year in gameFile:
                foundGameFile = gameFile
        if foundGameFile == None:
            raise Exception("Year "+year+" is not archived")
        f = open(gameFile, 'r')
        j = json.load(f) #a list of rounds
        preGame =[]
        year = gameFile[-4:]
        for r in j:
            gameRound = []
            for p in r:
                gameRound.append(p)
            preGame.append(gameRound)
        return preGame

    @classmethod
    def retrieveList(cls):
        games = []
        for gameFile in ConfigReader().listLegaNazionaleGames():
            f = open(gameFile, 'r')
            j = json.load(f) #a list of rounds
            preGame =[]
            year = gameFile[-4:]
            for r in j:
                gameRound = []
                for p in r:
                    gameRound.append(p)
                preGame.append(gameRound)
            games.append(cls(year, preGame))
        return sorted(games, key=lambda g: g.year)
            
            
if __name__ == '__main__':
    lista = Game.retrieveList()
    print (lista)