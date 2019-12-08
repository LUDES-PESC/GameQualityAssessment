'''
Created on 05/07/2015

@author: mangeli
'''
from GameQualityAssessment.code_pac.model import GenericGame, ItemTuple
import GameQualityAssessment.code_pac.brasileiro.model.game as BRmodel
from GameQualityAssessment.code_pac.measures.dramaByPointsUp2First import DramaByPointsUp2First

class BrasileiroGame(GenericGame):
    def __init__(self, game):
        if not isinstance(game, BRmodel.Game):
            raise TypeError('Arg must to be a brasileiro.model.Game instance')
        
        super(BrasileiroGame, self).__init__(game)
    
    def _setGameStruct(self,game):
        self._players = []
        self._gameData = []
        lastScore = {}
        
        gameRounds = self._game.gameRounds
        order = 1
        for gameRound in gameRounds:
            
            scores = []
            for score in gameRound:
                if not score.player in self._players:
                    self._players.append(score.player)
                    lastScore[score.player] = 0
                scores.append(ItemTuple(playerCode=score.player, roundScore= int(score.totalScore) - lastScore[score.player], totalScore=score.totalScore))
                lastScore[score.player] = score.totalScore
            self._gameData.append((order, scores))
            order +=1
            
if __name__ == "__main__":
    from GameQualityAssessment.code_pac.measures import DramaByPaths,DramaByPositionUp2First
    from GameQualityAssessment.code_pac.gamePlots import GamePlots
    import matplotlib.pyplot as plt
    import numpy as np
    
    list = BRmodel.Game.retrieveList()
    values=[]
    for game in list:
        g = BrasileiroGame(game)
        values.append([DramaByPaths(game=g, ignored=0).getMeasureValue(), 
                       DramaByPointsUp2First(game=g, ignored=0).getMeasureValue(),
                       DramaByPositionUp2First(game=g, ignored=0).getMeasureValue()])
    print (values[:])
    print (np.transpose(values))
    #p = GamePlots(game)
    #p.byPosition(ignored=0)
    plt.figure()
    plt.hist(np.transpose(values).reshape((12,3)),
             normed=False, 
             bins=5,
             range=[0,1],
             color=['red', 'green', 'blue'],
             label=['Path', 'Points', 'Position'])
    plt.legend()
    plt.show()
    
    
   