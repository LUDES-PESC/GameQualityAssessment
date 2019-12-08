'''
Created on 08/06/2015

@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac.measures import DramaByPointsUp2First, DramaByPositionUp2First, DramaByPaths
from time import sleep
from multiprocessing import Value, Process, Lock
from GameQualityAssessment.code_pac.model import DesafioGame
import dataBaseAdapter


def dramaAnalizerLocal(idt,game,counter,lock):
    lock.acquire()
    #print(idt," 1 - carrega modelo do jogo")
    aux_game_aux = DesafioGame(game)
    lock.release()

    lock.acquire()
    #print(idt," 2 - pega conexao")
    dao_connection = dataBaseAdapter.getConnection()
    lock.release()
    #valPoints = DramaByPointsUp2First(game=game_aux, ignored=1).getMeasureValue()
    #valPosition = DramaByPositionUp2First(game=game_aux, ignored=1).setIgnored(1).getMeasureValue()
    lock.acquire()
    #print(idt, " 3 - armazena o drama")
    game.storeMeasure(DramaByPointsUp2First(game=aux_game_aux, ignored=1), dao_connection)
    game.storeMeasure(DramaByPositionUp2First(game=aux_game_aux, ignored=1),dao_connection)
    game.storeMeasure(DramaByPaths(game=aux_game_aux, ignored=1),dao_connection)
    lock.release()
    
    lock.acquire()
    #print(idt," 4 - fecha a conexao")
    dataBaseAdapter.closeConnection(dao_connection)
    lock.release()

    lock.acquire()
    #print(idt," 5 - incrementa contador") 
    counter.value += 1
    lock.release()

    lock.acquire()
    #print(idt," 6 - retorna")
    lock.release()
    #return valPath (game, valPoints, valPosition, valPath)

def printFollow(counter, total):
    while True:
        print ("                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
        sleep(1))

def encapsulatedProcess(ind,games,len_games,counter,lock):
    if(ind >= len_games): return None
    game = games[ind]
    process = Process(target=dramaAnalizerLocal, args=(ind,game,counter,lock,), daemon=True)
    process.start()
    return process

def holdProcess(process):
    if(process == None): return
    if(process.is_alive()):
        process.join()
    process.close()

if __name__ == "__main__":

    from GameQualityAssessment.code_pac.desafio.model import Game, Tournament, Series

    connec = dataBaseAdapter.getConnection()
    jogos = []
    for torneio in Tournament.retriveList(connec):
        for serie in Series.retrieveList(torneio, connec):
            for jogo in Game.retrieveList(serie, connec):
                jogos.append(jogo)
    #print jogos[:]
    for jogo in jogos:
        if not isinstance(jogo, Game):
            print ('error')
    print (len(jogos))
    
    len_jogos = len(jogos)
    counter = Value('i', 0)
    lock = Lock()
    total = Value('i', len(jogos))
    p = Process(target=printFollow, args=(counter, total,))
    p.start()

    #pool = Pool(processes=3, initargs=(counter,))
    #r = pool.map(dramaAnalizerLocal, (jogos))
    for index in range(0,len_jogos,4):
        p1 = encapsulatedProcess(index,jogos,len_jogos,counter,lock)
        p2 = encapsulatedProcess(index+1,jogos,len_jogos,counter,lock)
        p3 = encapsulatedProcess(index+2,jogos,len_jogos,counter,lock)
        p4 = encapsulatedProcess(index+3,jogos,len_jogos,counter,lock)
        holdProcess(p1)
        holdProcess(p2)
        holdProcess(p3)
        holdProcess(p4)

    #drama = sum(r) / total.value
    #print ("")
    #print (drama)
    #pool.close()
    #pool.join()
    
    
    #print "                \r", counter.value, " -- ", counter.value / total.value * 100, "%",
    print ("")
    p.terminate()
    #print "drama: ", drama," | ", "maior: ", maior.value
    #gamePlots.GamePlots(desafioGame.DesafioGame(jogos[r.index(max(r))])).byPoints() 
    dataBaseAdapter.closeConnection(connec)