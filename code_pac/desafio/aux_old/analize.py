# -*- coding: utf-8 -*-
'''
Created on 21/05/2015

@author: mangeli
'''
from __future__ import division

from multiprocessing import Pool, Value, Lock, Array
from numpy.f2py.rules import aux_rules
import psycopg2.extras

import matplotlib.pyplot as plt
from modelo import *
import numpy as np


def analizeGame(game, connection):
    rodadas = sorted(GameRound.retrieveList(game, connection), key=lambda rodada: rodada.roundNumber)
    vencedor = sorted(GameRoundResult.retrieveList(rodadas[len(rodadas)-1], connection), key=lambda resultado: resultado.totalScore, reverse=True)[0].playerCode
    dist = 0
    count = 0
    for rodada in rodadas:
        '''a primeira rodada não tem resultados'''
        if not rodadas.index(rodada) == 0:
            '''resultados da rodada ordenados'''
            resultados = sorted(GameRoundResult.retrieveList(rodada, connection), key=lambda resultado: resultado.totalScore, reverse=True)
            '''se o vencedor não é o líder'''
            if not vencedor == resultados[0].playerCode:
                for r in resultados:
                    if r.playerCode == vencedor:
                        dist += resultados.index(r)
                        count +=1
                        break
    return dist / count if count > 0 else 0 

def analizeGameDrama(game):
    global maiorDramaJogo
    connection = psycopg2.connect("dbname=desafio_sebrae user=mangeli host=localhost password=agoravai")
    rodadas = sorted(GameRound.retrieveList(game, connection), key=lambda rodada: rodada.roundNumber)
    vencedor = sorted(GameRoundResult.retrieveList(rodadas[len(rodadas)-1], connection), key=lambda resultado: resultado.totalScore, reverse=True)[0].playerCode
    
    #with contador.get_lock():
    
    
    dist = 0
    count = 0
    for rodada in rodadas:
        '''a primeira rodada não tem resultados'''
        if not rodadas.index(rodada) == 0:
            '''resultados da rodada ordenados'''
            resultados = sorted(GameRoundResult.retrieveList(rodada, connection), key=lambda resultado: resultado.totalScore, reverse=True)
            '''se o vencedor não é o líder'''
            if not vencedor == resultados[0].playerCode:
                for r in resultados:
                    if r.playerCode == vencedor:
                        dist += (resultados[0].totalScore - r.totalScore) / resultados[0].totalScore
                        count += 1 
                        break
    connection.close()
    retorno = dist / count if count > 0 else 0
    #with maiorDrama.get_lock():
    #    with maiorDramaJogo.get_lock():
    l.acquire()
    contador.value += 1
    if retorno > maiorDrama.value:
        maiorDrama.value = retorno
        maiorDramaJogo[0] = game.tournamentCode
        maiorDramaJogo[1] = game.seriesCode
        maiorDramaJogo[2] = game.groupCode
    print "             \r", '%.2f' % ((contador.value / tamanho.value) * 100), "%", 
    l.release()
    
    return retorno

def printGameStory(game, connection):
    rodadas = sorted(GameRound.retrieveList(game, connection), key=lambda rodada: rodada.roundNumber)
    jogadores = []
    jogoObjeto = []
    for rodada in rodadas:
        #resultados da rodada ordenados
        resultados = sorted(GameRoundResult.retrieveList(rodada, connection), key=lambda resultado: resultado.totalScore, reverse=True)
        for r in resultados:
            if not r.playerCode in jogadores:
                jogadores.append(r.playerCode)
        
        #monta um dic do jogo, ordenado com as rodadas e a ordem dos jogadores 
        jogoObjeto.append((rodada.roundNumber, resultados))
        
    #pontuacao do jogador por rodada
    x = xrange(1, len(rodadas)+1)
    #plt.subplot(2,1,1)
    plt.figure()
    for jogador in jogadores:
        y=[]
        for i in range(0, len(jogoObjeto)):
            found = False
            for resultado in jogoObjeto[i][1]:
                if resultado.playerCode == jogador:
                    found = True
                    y.append(resultado.totalScore)
            if not found:
                y.append(float(0))
        plt.plot(x,y,'o-',linewidth=2)
    plt.ylabel(u'pontuação')
    plt.xlabel(u'rodada')    
    plt.show()
    
    
    
if __name__ == "__main__":
    
    conn = psycopg2.connect("dbname=desafio_sebrae user=mangeli host=localhost password=agoravai")
    
    jogos = []
    '''for torneio in Tournament.retriveList(conn):
        for fase in Series.retrieveList(torneio, conn):
            jogos += Game.retrieveList(fase, conn)'''
    torneio = Tournament.retriveList(conn)[2]
    fase = Series.retrieveList(torneio, conn)[3]
    jogos = Game.retrieveList(fase, conn)
    
    print "total de jogos: ", len(jogos)
    
    contador = Value('i', 0)
    tamanho = Value('i', len(jogos))
    maiorDrama = Value('f',0)
    maiorDramaJogo = Array('i', [jogos[0].tournamentCode, jogos[0].seriesCode, jogos[0].groupCode])
    l=Lock()
    print 'maiorDramaJogo antes: ', maiorDramaJogo[:]
    pool = Pool(processes=4, initargs=(contador,l,tamanho, maiorDrama, maiorDramaJogo,))
    resultado = pool.map(analizeGameDrama, (jogos))
    drama = sum(resultado) / len(resultado)
    
    pool.close()
    pool.join()
    
    print "drama: ", drama
    
    '''drama = 0
    maiorDrama = (jogos[0], analizeGameDrama(jogos[0], conn))
    for jogo in jogos:
        aux = analizeGameDrama(jogo, conn)
        drama += aux
        if aux > maiorDrama[1]:
            maiorDrama = (jogo, aux)
        print "                      ", "\r", jogos.index(jogo), "  de ", len(jogos),
    drama = drama / len(jogos)
    print drama'''
    print "maior drama", maiorDrama.value
    print maiorDramaJogo[:]
    torneio = Tournament.retrieve(maiorDramaJogo[0], conn)
    fase = Series.retrieve(torneio, maiorDramaJogo[1], conn)
    grupo = PlayerGroup.retrieve(torneio, maiorDramaJogo[2], conn)
    jogo = Game.retrieve(fase, grupo, conn)
    printGameStory(jogo, conn)