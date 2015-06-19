# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''

import psycopg2

import matplotlib.pyplot as plt
from modelo import Tournament, Series, Game, GameRound, GameRoundResult, PlayerGroup, Enrollment
import numpy as np


conn = psycopg2.connect("dbname=desafio_sebrae user=mangeli host=localhost password=agoravai")

#de um torneio
torneio = Tournament.retriveList(conn)[0]

#de uma fase
fase = Series.retrieveList(torneio, conn)[1]

#de um jogo
jogo = Game.retrieveList(fase, conn)[0]



'''monta os resultados do jogo'''
jogoObjeto = []
jogadores = []
pontos =[]
#rodadas
rodadas = sorted(GameRound.retrieveList(jogo, conn), key=lambda rodada: rodada.roundNumber)


for rodada in rodadas:
    #resultados da rodada ordenados
    resultados = sorted(GameRoundResult.retrieveList(rodada, conn), key=lambda resultado: resultado.totalScore, reverse=True)
    print rodada.roundNumber
    for r in resultados:
        print r.playerCode, " - ", r.totalScore
        if not r.playerCode in jogadores:
            jogadores.append(r.playerCode)
    
    #monta um dic do jogo, ordenada com as rodadas e a ordem dos jogadores 
    jogoObjeto.append((rodada.roundNumber, resultados))

  
#pontuacao do jogador por rodada
x = xrange(1, len(rodadas)+1)
plt.subplot(2,1,1)
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

#posicao por jogador por rodada
plt.subplot(2,1,2)
for jogador in jogadores:
    y=[]
    for i in range(0, len(jogoObjeto)):
        if i == 0: #todos começam na mesma posição
            #y.append(len(jogadores))
            y.append(1)
        else:
            found = False
            for resultado in jogoObjeto[i][1]:
                if resultado.playerCode == jogador:
                    found = True
                    y.append(jogoObjeto[i][1].index(resultado) + 1)
            if not found:
                y.append(len(jogadores))
    plt.plot(x,y,'o-',linewidth=2)
#plt.plot(x, np.zeros(len(x))) # inclui uma linha de zeros para faciliatar a leitura do gráfico
plt.ylim(0, len(jogadores)+1)
plt.ylabel(u'posição')
plt.xlabel(u'rodada')
plt.gca().invert_yaxis()    
plt.show()






print len(resultados)


#playerGroup desse jogo
playerGroupList = PlayerGroup.retrieveList(torneio, conn)

for playerGroup in playerGroupList:
    if playerGroup.tournamentCode == torneio.tournamentCode and playerGroup.groupCode == rodada.groupCode:
        grupo = playerGroup

#inscritos no grupo
inscritos = Enrollment.retrieveList(grupo, conn)

print len(inscritos) 