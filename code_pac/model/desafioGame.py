'''
Created on 07/06/2015

@author: mangeli
'''
from GameQualityAssessment.code_pac.model import GenericGame, ItemTuple
from GameQualityAssessment.code_pac import dataBaseAdapter
import GameQualityAssessment.code_pac.desafio.model as desafio_model

class DesafioGame(GenericGame):
    
    def __init__(self, game):
    
        if not isinstance(game, desafio_model):
            raise TypeError('Arg must to be a desafio.model.Game instance')
        
        super(DesafioGame, self).__init__(game)
        
    def _setGameStruct(self):
        connection = dataBaseAdapter.getConnection()
        self._players = []
        self._gameData = []
        
        gameRounds = sorted(desafio_model.GameRound.retrieveList(self._game, connection), key=lambda gameRound: gameRound.roundOrder)
        for gameRound in gameRounds:
            totalScores = sorted(desafio_model.GameRoundResult.retrieveList(gameRound, connection), key=lambda result: result.totalScore, reverse=True)
            scores = []
            for t in totalScores:
                scores.append(ItemTuple(t.playerCode, t.roundScore, t.totalScore))
                if not t.playerCode in self._players:
                    self._players.append(t.playerCode)
            
            self._gameData.append((gameRound.roundOrder, scores))
        dataBaseAdapter.closeConnection(connection)
        
if __name__ == "__main__":
    connection = dataBaseAdapter.getConnection()
    tournament = desafio_model.Tournament.retriveList(connection)[0]
    series = desafio_model.Series.retrieveList(tournament, connection)[0]
    game = desafio_model.Game.retrieveList(series, connection)[0]
    
    o = DesafioGame(game)
    print (o.getGameStruct())
    print (o.getLastRound())
    print (o.getNumberRounds())
    print (o.getPlayers())
    print (o.getRound(6))
    print (o.getWinner())