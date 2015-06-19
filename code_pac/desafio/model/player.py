# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''


import psycopg2.extras

from tournament import Tournament 


class Player:
    '''PlayerCode, TournamentCode is PK'''
    def __init__(self, tournament, playerCode, playerName, playerId, FU):
        if not isinstance(tournament, Tournament):
            raise TypeError('The first arg has to be a Tournament object')
        
        self.tournamentCode = tournament.tournamentCode
        self.playerCode = playerCode
        self.playerName = playerName
        self.playerID = playerId
        self.FU = FU
        self.tournament = tournament
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Player (playerCode, tournamentCode, playerName, playerId, FU)
                           VALUES (%(playerCode)s, %(tournamentCode)s, %(playerName)s, %(playerId)s, %(FU)s)""",
                           {'playerCode' : self.playerCode,
                            'tournamentCode' : self.tournamentCode,
                            'playerName' : self.playerName,
                            'playerId' : self.playerID,
                            'FU' : self.FU }
                            )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()

    @classmethod
    def retrieve(cls, tournament, playerCode, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("""SELECT * FROM Player WHERE tournamentCode = (%(tournamentCode)s) 
                        AND playerCode = (%(playerCode)s)""",
                       { 'tournamentCode' : tournament.tournamentCode,
                        'playerCode' : playerCode }
                       )
        retorno = cursor.fetchone()
        cursor.close()
        return cls(tournament, playerCode, retorno['playername'], retorno['playerid'], retorno['fu'])

    @classmethod
    def retriveList(cls, tournament, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM player WHERE tournamentCode = (%s)", (tournament.tournamentCode,))
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for player in preRetorno:
            retorno.append(Player(tournament, player['playercode'], player['playername'], player['playerid'], player['fu']))
        return retorno
