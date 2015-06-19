'''
Created on 08/06/2015

@author: mangeli
'''
from __future__ import division
from measures import DramaByPointsUp2First, DramaByPositionUp2First
from time import sleep
from multiprocessing import Value, Process, Pool
from code_pac.model import DesafioGame
import dataBaseAdapter


def dramaAnalizerLocal(game):
    conn = dataBaseAdapter.getConnection()
    game_aux = DesafioGame(game)
    valPoints = DramaByPointsUp2First(game_aux).getMeasureValue()
    valPosition = DramaByPositionUp2First(game_aux).getMeasureValue()
    game.storeMeasure(DramaByPointsUp2First(game_aux), conn)
    game.storeMeasure(DramaByPositionUp2First(game_aux),conn)
    dataBaseAdapter.closeConnection(conn)
    with counter.get_lock(): 
        counter.value += 1
    return (game, valPoints, valPosition)

def printFollow(counter, total):
    while True:
        print "                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
        sleep(0.01)
        
if __name__ == "__main__":

    import gamePlots
    from code_pac.desafio.model import Game, Tournament, Series
    conn = dataBaseAdapter.getConnection()
    jogos = []
    for torneio in Tournament.retriveList(conn):
        for serie in Series.retrieveList(torneio, conn):
            for jogo in Game.retrieveList(serie, conn):
                jogos.append(jogo)
    #print jogos[:]
    for jogo in jogos:
        if not isinstance(jogo, Game):
            print 'merda'
    
    counter = Value('i', 0)
    total = Value('i', len(jogos))
    p = Process(target=printFollow, args=(counter, total,))
    p.start()
    
    pool = Pool(processes=10, initargs=(counter,))
    r = pool.map(dramaAnalizerLocal, (jogos))
    drama = sum(r) / total.value
    
    pool.close()
    pool.join()
    #print "                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
    print ""
    p.terminate()
    #print "drama: ", drama," | ", "maior: ", maior.value
    #gamePlots.GamePlots(desafioGame.DesafioGame(jogos[r.index(max(r))])).byPoints() 
    dataBaseAdapter.closeConnection(conn)
    