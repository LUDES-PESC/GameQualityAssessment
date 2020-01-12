'''
Created on 08/06/2015

@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac.measures import DramaByPointsUp2First, DramaByPositionUp2First, DramaByPaths, LeadChange
from time import sleep
from multiprocessing import Value, Process, Pool
from GameQualityAssessment.code_pac.model import DesafioGame
import dataBaseAdapter



def dramaAnalizerLocal(game):
    conn = dataBaseAdapter.getConnection()
    game_aux = DesafioGame(game)
    
    #valPoints = DramaByPointsUp2First(game=game_aux, ignored=1).getMeasureValue()
    #valPosition = DramaByPositionUp2First(game=game_aux, ignored=1).setIgnored(1).getMeasureValue()
    #valPath = DramaByPaths(game=game_aux, ignored=1).getMeasureValue()
    valLeadChange = LeadChange(game=game_aux, ignored=1).getMeasureValue()
    #game.storeMeasure(DramaByPointsUp2First(game=game_aux, ignored=1), conn)
    #game.storeMeasure(DramaByPositionUp2First(game=game_aux, ignored=1),conn)
    #game.storeMeasure(DramaByPaths(game=game_aux, ignored=1),conn)
    game.storeMeasure(LeadChange(game=game_aux, ignored=1),conn)
    dataBaseAdapter.closeConnection(conn)
    with counter.get_lock(): 
        counter.value += 1
    return valLeadChange#(game, valPoints, valPosition, valPath)

def printFollow(counter, total):
    while True:
        print ("                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
        sleep(0.01))
        
if __name__ == "__main__":

    import GameQualityAssessment.code_pac.gamePlots
    from GameQualityAssessment.code_pac.desafio.model import Game, Tournament, Series
    conn = dataBaseAdapter.getConnection()
    jogos = []
    for torneio in Tournament.retriveList(conn):
        for serie in Series.retrieveList(torneio, conn):
            for jogo in Game.retrieveList(serie, conn):
                jogos.append(jogo)
    #print jogos[:]
    for jogo in jogos:
        if not isinstance(jogo, Game):
            print ('error')
    print (len(jogos))
    
    counter = Value('i', 0)
    total = Value('i', len(jogos))
    p = Process(target=printFollow, args=(counter, total,))
    p.start()
    
    pool = Pool(processes=3, initargs=(counter,))
    r = pool.map(dramaAnalizerLocal, (jogos))
    drama = sum(r) / total.value
    print ("")
    print (drama)
    pool.close()
    pool.join()
    
    dataBaseAdapter.closeConnection(conn)

    #print "                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
    print ("")
    p.terminate()
    #print "drama: ", drama," | ", "maior: ", maior.value
    #gamePlots.GamePlots(desafioGame.DesafioGame(jogos[r.index(max(r))])).byPoints() 
    dataBaseAdapter.closeConnection(conn)
    