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
import csv
from operator import itemgetter

ItemTuple = namedtuple("ItemTuple", ['player', 'totalScore'])

class Game:
    def __init__(self, gameNumber, gameRounds, fileName):
        self.gameNumber = gameNumber
        self.gameRounds = gameRounds
        self.fileName = fileName
        
    @classmethod
    def retrieveList(cls):
        games = []
        i = 0;
        for gameFile in ConfigReader().listDiceGames():
            with open(gameFile, 'rb') as csvfile:
                
                statFile = csv.reader(csvfile, delimiter=';', quotechar='|')
                statList = [];
                for line in statFile:
                    statList.append([int(line[0]), line[1], int(line[2])])
                statList.sort(key=itemgetter(2), reverse=True)
                statList.sort(key=itemgetter(0))
                roundNumber = -1;
                preGame =[]
                gameRound = [];
                for index,row in enumerate(statList):
                    if(roundNumber != row[0]):
                        if(index != 0):
                            preGame.append(gameRound);
                        roundNumber = row[0];
                        gameRound = [];
                    gameRound.append(ItemTuple(player=row[1], totalScore=int(row[2])))
                preGame.append(gameRound);
            games.append(cls(i, preGame, gameFile))
            i += 1
        return sorted(games, key=lambda g: g.gameNumber)
            
            
if __name__ == '__main__':
    lista = Game.retrieveList()
    print lista