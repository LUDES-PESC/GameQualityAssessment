'''
Created on 30/11/2015
ge
@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac.measures import MeasureTemplate, MeasureType
from GameQualityAssessment.code_pac.model import GenericGame
from GameQualityAssessment.code_pac.measures import probWinning

import math, sys


class UncertaintyEntropy(MeasureTemplate):
    '''
    evaluates the game Uncertainty by measure the distance between the
    discrete uniform distribution of the probabilities of players win
    the game and the actual probability distribution vis a vis the normalized
    score relation
    '''


    def __init__(self, *args, **kwargs):
        if kwargs.get('scoreLimit') == None:
            self._probPlayer = probWinning.probA
        else:
            self._probPlayer = probWinning.probB
            self._scoreLimit = kwargs.get('scoreLimit')
            
        super(UncertaintyEntropy, self).__init__(*args, **kwargs)
        self._measureType = MeasureType(code=4, description='Uncertainty by Entropy', version=1) #for retro compatibility
        #some games have a limit in the score increasing per turn
        

    def _evaluateMeasure(self):
        nPlayers = len(self._game.getPlayers())
        self._nTurns = self._game.getNumberRounds() - self._ignored #first gameRound hasn't results
        
        if nPlayers == 0 or self._nTurns == 0:
            self._measureValue = 0 #preventing possible garbage in dataset
        else:
            players = self._game.getPlayers() #list of players
            nPlayers = len(players)
            
                        
            matchUncertainty = 0
            
            
            for gameRound in self._game.getGameStruct():
                inPlayers = []
                turnScores={}
                turnCertainty = 0
                self._turnNumber = self._game.getGameStruct().index(gameRound) + 1
                
                '''first gameRound hasn't results, last gameRound is discarded'''
                if self._turnNumber > self._ignored \
                    and self._turnNumber < self._game.getNumberRounds(): #starting from 0, stoping before the last
                    '''for debug'''
                    #testProb = 0
                    #print '---------------', self._turnNumber
                    #building round players list and top score in the turn
                    for roundItem in gameRound[1]:
                        inPlayers.append(roundItem.playerCode)
                        turnScores[roundItem.playerCode] = max(0, roundItem.totalScore - self._minScore)
                        turnUncertaintyPart = 0
                            
                    for player in players:
                        if player in inPlayers:
                            proPlayer = self._probPlayer(player, turnScores, self) #(turnScores[player]/totalRoundScore) #probability of the player win the match
                            turnUncertaintyPart += proPlayer*math.log(proPlayer,2) / math.log(nPlayers,2)
                        else:
                            proPlayer = 0
                            turnUncertaintyPart += proPlayer
                            
                        '''for debug'''
                        #testProb += proPlayer
                        #print player, turnScores.get(player), proPlayer
                    
                    turnUncertainty = - turnUncertaintyPart
                    matchUncertainty += turnUncertainty
                    #print turnUncertainty, testProb
                            
            self._measureValue = (matchUncertainty / (self._nTurns - 1))
                
if __name__ == '__main__':
    import GameQualityAssessment.code_pac.brasileiro.model as brasileiroModel
    import GameQualityAssessment.code_pac.model as model
    import GameQualityAssessment.code_pac.measures as measures
    
    from GameQualityAssessment.code_pac import dataBaseAdapter
    import GameQualityAssessment.code_pac.desafio.model as desafioModel
    
    #set the test type (brasileiro = 1, desafio = 2)
    testType = 2
    
    #set desafioGame data
    tournamentCode = 160
    seriesCode = 296
    groupCode = 64117
    
    
    if testType == 1:
        games = brasileiroModel.Game.retrieveList()
        for game in games:
            print (game.year)
            print (measures.UncertaintyEntropy(game=model.BrasileiroGame(game), ignored=0, scoreLimit=3).getMeasureValue())
            print ('===================')
    elif testType == 2:
        conn = dataBaseAdapter.getConnection()
        tournament = desafioModel.Tournament.retrieve(tournamentCode, conn)
        series = desafioModel.Series.retrieve(tournament, seriesCode, conn)
        game = desafioModel.Game(series, groupCode)
        print (tournament.refYear)
        print (measures.UncertaintyEntropy(game=model.DesafioGame(game), ignored=1, minScore=10).getMeasureValue())
        print ('================')
    
