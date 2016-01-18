'''
Created on 30/11/2015

@author: mangeli
'''
from __future__ import division
from code_pac.measures import MeasureTemplate, MeasureType
from code_pac.model import GenericGame

import math


class Uncertainty(MeasureTemplate):
    '''
    evaluates the game Uncertainty by measure the probability of players win the game based on their
    relative position to the leader
    '''


    def __init__(self, *args, **kwargs):
        super(Uncertainty, self).__init__(*args, **kwargs)
        self._measureType = MeasureType(code=3, description='Uncertainty', version=1) #for retro compatibility

    def _evaluateMeasure(self):
        nPlayers = len(self._game.getPlayers())
        nTurns = self._game.getNumberRounds() - self._ignored #first gameRound hasn't results
        
        if nPlayers == 0 or nTurns == 0:
            self._measureValue = 0 #preventing possible garbage in dataset
        else:
            players = self._game.getPlayers() #list of players
            winner = self.getWinner()
                        
            positionHistory = {} #alternative method
            scoresHistory = {}
            turnCounter = 0
            
            for player in players:
                positionHistory[player] = []
                scoresHistory[player] = []
        
            for gameRound in self._game.getGameStruct():
                inPlayers = []
                roundScores={}
                topScore = 0
                '''first gameRound hasn't results'''
                if self._game.getGameStruct().index(gameRound) > self._ignored - 1: #starting from 0
                    turnCounter += 1
                    turnDrama = 0
                    #building round players list and top score in the turn
                    for roundItem in gameRound[1]:
                        inPlayers.append(roundItem.playerCode)
                        roundScores[roundItem.playerCode] = roundItem.roundScore 
                        if roundItem.roundScore > topScore:
                            topScore = roundItem.roundScore
                            
                    for player in positionHistory.keys():
                        #filling scoresHistory with values from this turn
                        if player in inPlayers:
                            positionHistory[player].append(inPlayers.index(player) + 1)
                            scoresHistory[player].append(roundScores[player]/topScore) 
                        else: #player is eliminated
                            positionHistory[player].append(0) 
                            scoresHistory[player].append(0)
                        #computing turn drama
                        
                    
            
            self._measureValue = 0
            
    def _getExpectedScore(self, scores):
        '''the expected score of a player'''
        return sum(scores) / float(len(scores))
    
    def _getSigma(self, scores, eScore):
        '''the standard deviation of players score'''
        aux = 0
        for score in scores:
            aux += (score - eScore)**2
        return math.sqrt(aux / float(len(scores)))
        
    def _getWinningProb(self, player, scoresHistory):
        '''the probabilita of winning for a given player'''
        eScore = self._getExpectedScore(scoresHistory[player])
        pSigma = self._getSigma(scoresHistory[player], eScore)
        return (1-eScore) / pSigma

if __name__ == '__main__':
    import code_pac.brasileiro.model as brasileiroModel
    import code_pac.model as model
    import code_pac.measures as measures
    
    from code_pac import dataBaseAdapter
    import code_pac.desafio.model as desafioModel
    
    #set the test type (brasileiro = 1, desafio = 2)
    testType = 2
    
    #set desafioGame data
    tournamentCode = 123
    seriesCode = 264
    groupCode = 10886
    
    
    if testType == 1:
        games = brasileiroModel.Game.retrieveList()
        for game in games:
            print game.year
            print measures.Uncertainty(game=model.BrasileiroGame(game), ignored=0).getMeasureValue()
            print '==================='
    elif testType == 2:
        conn = dataBaseAdapter.getConnection()
        tournament = desafioModel.Tournament.retrieve(tournamentCode, conn)
        series = desafioModel.Series.retrieve(tournament, seriesCode, conn)
        game = desafioModel.Game(series, groupCode)
        print tournament.refYear
        print measures.Uncertainty(game=model.DesafioGame(game), ignored=1).getMeasureValue()
        print '================'
    
