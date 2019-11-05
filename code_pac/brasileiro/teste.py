'''
Created on 05/07/2015

@author: mangeli
'''
from GameQualityAssessment.code_pac.brasileiro.model.game import Game
from GameQualityAssessment.code_pac.model import BrasileiroGame
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from GameQualityAssessment.project_path import make_absolute_path as abspath
from GameQualityAssessment.code_pac.measures import DramaByPaths, DramaByPositionUp2First, DramaByPointsUp2First

if __name__ == '__main__':
    wb = Workbook()
    planilha = wb.active
    planilha.append(['ano','Drama by Path', 'Drama by Points', 'Drama by position'])
    games = Game.retrieveList()
    for game in games:
        genGame = BrasileiroGame(game)
        
        dramaPath = DramaByPaths(game=genGame, ignored=0).getMeasureValue() 
        dramaPoints = DramaByPointsUp2First(game=genGame, ignored=0, normScores=True).getMeasureValue()
        dramaPosition = DramaByPositionUp2First(game=genGame, ignored=0).getMeasureValue()
        planilha.append([game.year, dramaPath, dramaPoints, dramaPosition])
        
        
        winner = genGame.getWinner()
        nPlayers = len(genGame.getPlayers())
        nRounds = genGame.getNumberRounds()
        winnerPath = []
        for i in range(1, nRounds + 1):
            gameRound = genGame.getRound(i)[1]
            for r in gameRound:
                if r.playerCode == winner:
                    winnerPath.append(gameRound.index(r)+1)
                    break
        plt.figure(game.year)
        plt.plot(np.arange(1,nRounds+1), winnerPath, '-b', linewidth=1.5)
        plt.xlim(1,nRounds)
        plt.ylim(0, nPlayers)
        plt.yticks(np.arange(1, nPlayers, 3))
        plt.gca().invert_yaxis()
        plt.gca().set_title(str(game.year))
        fString = '{0:.4f}'
        plt.gca().text(0.63,0.02,'Drama by Path: ' + fString.format(dramaPath) + '\n'
                       + 'Drama by Points: ' + fString.format(dramaPoints) + '\n'
                       + 'Drama by Position: ' + fString.format(dramaPosition)
                       ,transform=plt.gca().transAxes,
                       verticalalignment='bottom', horizontalalignment='left')
    plt.show()
    wb.save(abspath('dadosDrama.xlsx'))