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
    evaluates the game Uncertainty by measure the distance between the
    discrete uniform distribution of the probabilities of players win
    the game and the actual probability distribution vis a vis the normalized
    score relation
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
            nPlayers = len(players)
            #winner = self.getWinner()
                        
            probabilitiesHistory = []
            turnCounter = 0
            
            for gameRound in self._game.getGameStruct():
                inPlayers = []
                normScores = []
                probabilities = []
                roundScores={}
                topScore = 0
                '''first gameRound hasn't results'''
                if self._game.getGameStruct().index(gameRound) > self._ignored - 1: #starting from 0
                    turnCounter += 1
                    #building round players list and top score in the turn
                    for roundItem in gameRound[1]:
                        inPlayers.append(roundItem.playerCode)
                        roundScores[roundItem.playerCode] = roundItem.roundScore
                        if roundItem.roundScore > topScore:
                            topScore = roundItem.roundScore
                            
                    for player in players:
                        if player in inPlayers:
                            normScore = (roundScores[player]/topScore) #normalized score 
                        else:
                            normScore = 0
                        normScores.append(normScore)
                    
                    for score in normScores:
                        probabilities.append(score/sum(normScores))
                    
                    probabilitiesHistory.append(probabilities)
            
            
                
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
    seriesCode = 272
    groupCode = 13379
    
    
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
    
