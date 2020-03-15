'''
Created on 05/07/2015

@author: mangeli
'''
from GameQualityAssessment.code_pac.model import GenericGame, ItemTuple
import GameQualityAssessment.code_pac.italiano.model.game as ITmodel

class LegaNazionaleGame(GenericGame):
    def __init__(self, game):
        if not isinstance(game, ITmodel.Game):
            raise TypeError('Arg must to be a brasileiro.model.Game instance')
        self._winner = None
        super(LegaNazionaleGame, self).__init__(game)
    
    def _setGameStruct(self):
        self._players = []
        self._gameData = []
        lastScore = {}
        
        gameRounds = self._game.gameRounds
        order = 1
        for gameRound in gameRounds:
            
            scores = []
            for score in gameRound:
                if not score[0] in self._players:
                    self._players.append(score[0])
                    lastScore[score[0]] = 0
                scores.append(ItemTuple(playerCode=score[0], roundScore= int(score[1]) - lastScore[score[0]], totalScore=score[1]))
                lastScore[score[0]] = score[1]
            self._gameData.append((order, scores))
            order +=1
            
if __name__ == "__main__":
    from GameQualityAssessment.code_pac.measures import DramaByPaths,DramaByPositionUp2First,DramaByPointsUp2First
    from GameQualityAssessment.code_pac.gamePlots import GamePlots
    import matplotlib.pyplot as plt
    import numpy as np
    
    the_list = ITmodel.Game.retrieveList()
    values=[]
    for game in the_list:
        g = LegaNazionaleGame(game)
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
