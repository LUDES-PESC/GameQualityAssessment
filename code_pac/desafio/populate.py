# -*- coding: utf-8 -*-
from __future__ import division

from code_pac import dataBaseAdapter as db
from multiprocessing import Pool, Value, Lock
from parser import Parser

import model


def procDataLines(dataLine):
    
    db.setValues('desafio_simples', 'mangeli', 'localhost', 'agoravai', 5432)
    conn = db.getConnection() 
    
    tournament = model.Tournament(int(dataLine[5]), dataLine[2], int(dataLine[1]), dataLine[0])
    tournament.store(conn)
    
    player = model.Player(tournament, int(dataLine[8]), dataLine[14], dataLine[13], dataLine[16])
    player.store(conn)
    
    series = model.Series(tournament, int(dataLine[6]), int(dataLine[3]))
    series.store(conn)
    
    game = model.Game(series, int(dataLine[7]))
    game.store(conn)
    
    enrollment = model.Enrollment(player, int(dataLine[7]), int(dataLine[6]), dataLine[20])
    enrollment.store(conn)
    
    gameRound = model.GameRound(game, int(dataLine[9]), int(dataLine[4]))
    gameRound.store(conn)
    
    
    roundResult = model.GameRoundResult(gameRound, enrollment, dataLine[18], dataLine[19], dataLine[11])
    roundResult.store(conn)
    
    with contador.get_lock():
        contador.value += 1
    l.acquire()
    #print str((contador.value / tamanho.value) * 100), " %", "                                \r",
    print "             \r", '%.2f' % ((contador.value / tamanho.value) * 100), "%", 
    l.release()
    
    conn.close()


if __name__ == "__main__":

    #abre o arqruivo
    parser = Parser('../../data/desafio/raw_data/dados.xlsx')
    
    #le o arquivo
    linhas = parser.getValues(0, 0) #planilha 0 com zero linhas de cabecalho
    
    
    print len(linhas)
    #imprime a associacao entre índice e nome do campo
    #for i in range(len(linhas[0])):
    #    print str(i) + ' - ' + linhas[0][i]
    
    #for i in linhas:
    #    print i
        
    #for i in range(len(linhas)):
    #    print "linha ", str(i+1), " de ", str(len(linhas)) + "\r",
    
    contador = Value('i', 0)
    tamanho = Value('i', len(linhas))
    l=Lock()
    pool = Pool(processes=4, initargs=(contador,l,tamanho,))
    pool.map(procDataLines, (linhas))
    pool.close()
    pool.join()
    '''print linhas[0][:]
    procDataLines(linhas[0])'''
