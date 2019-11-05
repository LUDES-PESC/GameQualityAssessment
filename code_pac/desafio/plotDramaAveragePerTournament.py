'''
Created on 02/10/2015

@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac import dataBaseAdapter as db, measures
from GameQualityAssessment.code_pac.desafio.model import Tournament, Series, Game
from GameQualityAssessment.project_path import make_absolute_path as abspath
import csv
import matplotlib as mpl
#from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import *
import matplotlib.pyplot as plt
import numpy as np

def plot3DDrama(gamesInput):
    x=[]
    y=[]
    z=[]
    for g in gamesInput:
        x.append(g.get('dramapoints'))
        y.append(g.get('dramaposition'))
        z.append(g.get('dramapaths'))
    
    fig = plt.figure(gamesInput[0].get('tournamentcode'))
    ax = fig.gca(projection='3d')
    
    ax.scatter(x,y,z)
    return fig


def getValidGames(seriesInput, arq):
    games = []
    for linha in arq:
        if not arq.line_num == 1 and \
           int(linha[1]) == seriesInput.seriesCode and \
           int(linha[0]) == seriesInput.tournamentCode: #ignores first line and series other than seriesInput
           
            tournament = Tournament.retrieve(linha[0], conn)
            series = Series.retrieve(tournament, linha[1], conn)
            groupCode = linha[2]
            game = Game(series, groupCode)
            games.append(game)
    return games



def plotHist(measures):
    mDPoints = []
    mDPositions = []
    mDPaths = []
    
    for m in measures:
        mDPoints.append(m.get('dramapoints'))
        mDPositions.append(m.get('dramaposition'))
        mDPaths.append(m.get('dramapaths'))
    tournament = measures[0].get('game').tournament
    series = measures[0].get('game').series
    title = str(tournament.country).strip() + ' ' + str(tournament.refYear) + ' series:'  + str(series.seriesOrder)
    fig = plt.figure(title)
    #ax = fig.gca()
    plt.hist([mDPoints,mDPositions,mDPaths], color=['m','b','c'], label=['Drama by Points', 'Drama by Position', 'Drama by Paths'])
    plt.title(title)
    plt.legend(fontsize='medium', loc=7)
    return fig
    
def getMeasureValues(games):
    measures = []
    for game in games:
        dramaMeasures = game.retrieveMeasureList(conn, 'last')
        preAdd={'game' : game}
        for m in dramaMeasures:
                if m.get('measuredescription') == 'Drama by points':
                    preAdd['dramapoints'] = m.get('measurevalue')
                
                elif m.get('measuredescription') == 'Drama by position':
                    preAdd['dramaposition'] = m.get('measurevalue')
    
                elif m.get('measuredescription') == 'Drama by paths':
                    preAdd['dramapaths'] = m.get('measurevalue')
        measures.append(preAdd)
    return measures
    
if __name__ == '__main__':
    db.setValues('desafio_simples', 'mangeli', 'localhost', 'agoravai', 5432)
    conn = db.getConnection()
    dbCursor = db.getCursor(conn)
    
    #reading valid games
    print ("Reading valid games csv...")
    
    
    '''
    tournamentsCodes = set()    #set of tournamentcodes with valid games
    seriesCodes = set()         #set of series ([tournamentCode, seriesCode]) with valid games
    games =[]                   #list of all valid games
    detailedGames=[]            #list of all valid games and its drama measure values
    '''
       
    #retrieving drama information from db
    print ("Retrieving drama information from db...")
    targets = [(123,272), (123,264), (160,296), (160,303), (166,313), (166,324), (127,281), (127,291)]
    for target in targets:
        arq = csv.reader(open(abspath("../../data/desafio/raw_data/valid_games.csv"), "r"), delimiter=";")
        t = Tournament.retrieve(target[0], conn)
        games = getValidGames(Series.retrieve(t, target[1], conn), arq)
        values = getMeasureValues(games)
        plotHist(values)
    plt.show()
    '''for linha in arq:
        if (not arq.line_num == 1): #ignores first line
            tournamentsCodes.add(linha[0])
            seriesCodes.add((linha[0], linha[1]))
            
            tournament = Tournament.retrieve(linha[0], conn)
            series = Series.retrieve(tournament, linha[1], conn)
            groupCode = linha[2]
            game = Game(series, groupCode)
            
            games.append(game)
            
            dramaMeasures = game.retrieveMeasureList(conn, 'last')
            preAdd = {'tournamentcode' : dramaMeasures[0].get('tournamentcode'),
                      'seriescode'     : dramaMeasures[0].get('seriescode'),
                      'groupcode'      : dramaMeasures[0].get('groupcode')}
            
            for m in dramaMeasures:
                if m.get('measuredescription') == 'Drama by points':
                    preAdd['dramapoints'] = m.get('measurevalue')
                
                elif m.get('measuredescription') == 'Drama by position':
                    preAdd['dramaposition'] = m.get('measurevalue')
    
                elif m.get('measuredescription') == 'Drama by paths':
                    preAdd['dramapaths'] = m.get('measurevalue')
                    
            detailedGames.append(preAdd)
    
    print "Ploting..."
    for t in sorted(list(tournamentsCodes)):
        v = [g for g in detailedGames if g.get('tournamentcode') == int(t)]
        if len(v) > 0:
            plotDrama(v)
        
    plt.show()
        
    '''
    
    '''get tournament codes
    db.cursorExecute(dbCursor, "select distinct tournamentcode from tournament")
    tournamentCodes = db.fetchAll(dbCursor)'''
    
    
    