'''
Created on 08/06/2015

@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac.measures import UncertaintyPDD
from time import sleep
from multiprocessing import Value, Process, Lock
from GameQualityAssessment.code_pac.model import DesafioGame
import GameQualityAssessment.code_pac.dataBaseAdapter as dataBaseAdapter



def storeUncertainty(ind,game,counter,lock):
    lock.acquire()
    conn = dataBaseAdapter.getConnection()
    lock.release()
    lock.acquire()
    game_aux = DesafioGame(game)
    lock.release()
    
    #valPoints = DramaByPointsUp2First(game=game_aux, ignored=1).getMeasureValue()
    #valPosition = DramaByPositionUp2First(game=game_aux, ignored=1).setIgnored(1).getMeasureValue()
    #valPath = DramaByPaths(game=game_aux, ignored=1).getMeasureValue()
    #valLeadChange = LeadChange(game=game_aux, ignored=1).getMeasureValue()
    
    #try:
    #    valUncertainty = UncertaintyPDD(game=game_aux, ignored=1, minScore=50).getMeasureValue()
    #except:
    #    print ('Error:', game.tournamentCode, ' ', game.seriesCode, ' ', game.groupCode)
    
    #game.storeMeasure(DramaByPointsUp2First(game=game_aux, ignored=1), conn)
    #game.storeMeasure(DramaByPositionUp2First(game=game_aux, ignored=1),conn)
    #game.storeMeasure(DramaByPaths(game=game_aux, ignored=1),conn)
    lock.acquire()
    game.storeMeasure(UncertaintyPDD(game=game_aux, ignored=1, minScore=50),conn)
    lock.release()
    lock.acquire()
    dataBaseAdapter.closeConnection(conn)
    lock.release()
    lock.acquire() 
    counter.value += 1
    lock.release()
    #return valUncertainty#(game, valPoints, valPosition, valPath)

def printFollow(counter, total,lock):
    while True:
        lock.acquire()
        print ("                \r", counter.value, " -- ", counter.value / total.value * 100, "%")
        lock.release()
        sleep(5)


def encapsulatedProcess(ind,games,len_games,counter,lock):
    if(ind >= len_games): return None
    game = games[ind]
    process = Process(target=storeUncertainty, args=(ind,game,counter,lock,), daemon=True)
    process.start()
    return process

def holdProcess(process):
    if(process == None): return
    if(process.is_alive()):
        process.join()
    process.close()

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
    
    lock = Lock()
    counter = Value('i', 0)
    total = Value('i', len(jogos))
    p = Process(target=printFollow, args=(counter, total,lock,))
    p.start()

    len_jogos = len(jogos)

    for index in range(0,len_jogos,4):
        p1 = encapsulatedProcess(index,jogos,len_jogos,counter,lock)
        p2 = encapsulatedProcess(index+1,jogos,len_jogos,counter,lock)
        p3 = encapsulatedProcess(index+2,jogos,len_jogos,counter,lock)
        p4 = encapsulatedProcess(index+3,jogos,len_jogos,counter,lock)
        holdProcess(p1)
        holdProcess(p2)
        holdProcess(p3)
        holdProcess(p4)
    
    #pool = Pool(processes=3, initargs=(counter,))
    #r = pool.map(storeUncertainty, (jogos))
    #drama = sum(r) / total.value
    print ("")
    #print (drama)
    #pool.close()
    #pool.join()
    
    #dataBaseAdapter.closeConnection(conn)

    #print "                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
    print ("")
    p.terminate()
    #print "drama: ", drama," | ", "maior: ", maior.value
    #gamePlots.GamePlots(desafioGame.DesafioGame(jogos[r.index(max(r))])).byPoints() 
    dataBaseAdapter.closeConnection(conn)
    