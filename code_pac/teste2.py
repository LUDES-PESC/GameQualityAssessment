'''
Created on 11/06/2015

@author: mangeli
'''
from __future__ import division
from measures import DramaByPointsUp2First, DramaByPositionUp2First
from time import sleep
from multiprocessing import Value, Process, Pool
from code_pac.model import DesafioGame
import dataBaseAdapter
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
    
    game_aux = DesafioGame(jogo)
    print 'i'
    valPoints = DramaByPointsUp2First(game_aux).getMeasureValue()
    jogo.storeMeasure(DramaByPointsUp2First(jogo), conn)
