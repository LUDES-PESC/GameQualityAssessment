'''
Created on 05/07/2015

@author: mangeli
'''
from GameQualityAssessment.code_pac.model import GenericGame, ItemTuple
import GameQualityAssessment.code_pac.pontosCorridos.model.game as PCmodel
from GameQualityAssessment.code_pac.measures.dramaByPointsUp2First import DramaByPointsUp2First

class PontosCorridosGame(GenericGame):
    def __init__(self, game):
        if not isinstance(game, PCmodel.Game):
            raise TypeError('Arg must to be a pontosCorridos.model.Game instance')
        
        super(PontosCorridosGame, self).__init__(game)
    
    def _setGameStruct(self):
        self._players = []
        self._gameData = []
        lastScore = {}
        
        gameRounds = self._game.gameRounds
        order = 1
        for gameRound in gameRounds:
            
            scores = []
            for score in gameRound:
                player = score[0]
                points = score[1]
                if not player in self._players:
                    self._players.append(player)
                    lastScore[player] = 0
                scores.append(ItemTuple(playerCode=player, roundScore= int(points) - lastScore[player], totalScore=points))
                lastScore[player] = points
            self._gameData.append((order, scores))
            order +=1
            
if __name__ == "__main__":
    from GameQualityAssessment.code_pac.measures import DramaByPaths,DramaByPositionUp2First
    from GameQualityAssessment.code_pac.gamePlots import GamePlots
    import matplotlib.pyplot as plt
    import numpy as np
    
    list = PCmodel.Game.retrieveList('all')
    values=[]
    for game in list:
        g = PontosCorridosGame(game)
        values.append([DramaByPaths(game=g, ignored=0).getMeasureValue(), 
                       DramaByPointsUp2First(game=g, ignored=0).getMeasureValue(),
                       DramaByPositionUp2First(game=g, ignored=0).getMeasureValue()])
    print (values[:])
    print (np.transpose(values))
    #p = GamePlots(game)
    #p.byPosition(ignored=0)
    plt.figure()
    plt.hist(np.transpose(values).reshape((len(values),3)),
             normed=False, 
             bins=5,
             range=[0,1],
             color=['red', 'green', 'blue'],
             label=['Path', 'Points', 'Position'])
    plt.legend()
    plt.show()
    
    
   