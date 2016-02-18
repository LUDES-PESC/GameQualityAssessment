'''
Created on 18/02/2016

@author: mangeli
'''
from __future__ import division

def probA(player, turnScores, measure):
        return turnScores[player] / sum(turnScores.values())
    
def probB(player, turnScores, measure):
    adjustedScores = {}
    for p in turnScores.keys():
        adjustedScores[p] = turnScores[p]*_achievementTest(p, turnScores, measure)
    return adjustedScores[player] / sum(adjustedScores.values())

def _achievementTest(player, turnScores, measure):
        remainingTurns = measure._game.getNumberRounds() - measure._turnNumber
        maxScoreUntilEnd = measure._scoreLimit * remainingTurns
        scoreGap = max(turnScores.values()) - turnScores[player]
        if scoreGap > maxScoreUntilEnd:
            adjust = 0
        else:
            adjust = 1 /( 1 + scoreGap)
        return adjust  

if __name__ == '__main__':
    pass