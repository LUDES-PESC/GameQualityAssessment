# -*- coding: utf-8 -*-
import psycopg2

from GameQualityAssessment.code_pac.desafio.model import Tournament, Player, Series, Game, GameRound, Enrollment, GameRoundResult


conn = psycopg2.connect("dbname=desafio_sebrae user=mangeli host=localhost password=agoravai")


#recupera lista de torneios
torneios = Tournament.retriveList(conn)

#recupera o codigo do primeiro torneio da lista
codigoTorneio = torneios[0].tournamentCode

# monta um torneio com o codigo anterior
# ATENÇÃO: desnecessário, esse é um exemplo de demonstação. O primeiro item da lista anterior já um objeto com esses valores
torneio = Tournament.retrieve(codigoTorneio, conn)

# dados de um torneio
playerList = Player.retriveList(torneio, conn)

seriesList = Series.retrieveList(torneio, conn)

series = seriesList[0]

#playerGroupList = PlayerGroup.retrieveList(torneio, conn)
playerGroupList = []

gameList = Game.retrieveList(series, conn)

game = gameList[0]

gameRoundList = GameRound.retrieveList(game, conn)

enrollmentList = Enrollment.retrieveList(playerGroupList[1], conn)

roundResultList = GameRoundResult.retrieveList(gameRoundList[0], conn)

print (roundResultList[1].roundScore)

