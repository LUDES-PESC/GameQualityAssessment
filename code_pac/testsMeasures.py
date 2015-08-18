# -*- coding: utf-8 -*-
'''
Created on 14/07/2015

@author: mangeli
'''
from code_pac import dataBaseAdapter
from code_pac.gamePlots import GamePlots
import code_pac.desafio.model as desafioModel
import code_pac.model as model
from code_pac.measures import DramaByPaths, DramaByPointsUp2First
import code_pac.brasileiro.model as brasileiroModel
   
if __name__ == '__main__':
    '''
    connection = dataBaseAdapter.getConnection()
    tournament = desafioModel.Tournament.retriveList(connection)[0]
    series = desafioModel.Series.retrieveList(tournament, connection)[1]
    '''
    #game = desafioModel.Game.retrieveList(series, connection)[1]
    game = brasileiroModel.Game.retrieveList()[2]
    #obj = model.DesafioGame(game)
    obj = model.BrasileiroGame(game)
    value = DramaByPointsUp2First(game=obj, ignored=0, normScores=True)
    #game.storeMeasure(value,connection)
    print value.getWinner(), value.getMeasureValue()
    
    print value.getType().description
    #print game.tournamentCode, " ", game.seriesCode, " ", game.groupCode
    '''dataBaseAdapter.closeConnection(connection)'''
    GamePlots(obj).byPoints()