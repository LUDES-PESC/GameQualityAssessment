# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''

import psycopg2.extras

from player import Player


class Enrollment:
    '''GroupCode, TournamentCode, PlayerCode is PK'''
    
    def __init__(self, player, groupCode, seriesCode, finalScore):
        if not isinstance(player, Player):
            raise TypeError('The first arg has to be a Player object')
                
        self.groupCode = groupCode
        self.playerCode = player.playerCode
        self.tournamentCode = player.tournamentCode
        self.finalScore = finalScore
        self.seriesCode = seriesCode
        self.player = player
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Enrollment (groupCode, tournamentCode, playerCode, seriesCode, finalScore)
                           VALUES (%(groupCode)s, %(tournamentCode)s, %(playerCode)s, %(seriesCode)s, %(finalScore)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'groupCode' : self.groupCode,
                            'playerCode' : self.playerCode,
                            'seriesCode' : self.seriesCode,
                            'finalScore' : self.finalScore}
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()

    @classmethod
    def retrieve(cls, player, groupCode, seriesCode, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("""SELECT * FROM Enrollment WHERE tournamentCode = (%(tournamentCode)s) 
                        AND playerCode = (%(playerCode)s)
                        AND groupCode = (%(groupCode)s)""",
                       { 'tournamentCode' : player.tournamentCode,
                        'playerCode' : player.playerCode,
                        'seriesCode' : seriesCode,
                        'groupCode' : groupCode }
                       )
        retorno = cursor.fetchone()
        cursor.close()
        return cls(player, retorno['groupcode'], retorno['seriescode'], retorno['finalscore'])
    
    @classmethod
    def retrieveList(cls, player, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT * FROM Enrollment WHERE tournamentCode = (%(tournamentCode)s)
                        AND playerCode = (%(playerCode)s) """, 
                        {'tournamentCode' : player.tournamentCode,
                         'playerCode' : player.playerCode}
                        )
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for enrollment in preRetorno:
            retorno.append(Enrollment(player, enrollment['groupCode'], enrollment['seriesCode'], enrollment['finalscore']))
        return retorno 
