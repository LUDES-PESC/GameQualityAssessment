# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''
import psycopg2.extras
from game import Game


class GameRound:
    '''RoundCode, TournamentCode, SeriesCode, GroupCode is PK'''
  
    def __init__(self, game, roundCode, roundOrder):
        if not isinstance(game, Game):
            print game
            raise TypeError('The first arg has to be a Game object')
        
        self.roundCode = roundCode
        self.tournamentCode = game.tournamentCode
        self.seriesCode = game.seriesCode
        self.groupCode = game.groupCode
        self.roundOrder = roundOrder
        self.game = game
        self.tournament = game.tournament
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO GameRound (roundCode, tournamentCode, seriesCode, groupCode, roundOrder)
                           VALUES (%(roundCode)s, %(tournamentCode)s, %(seriesCode)s, %(groupCode)s, %(roundOrder)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'groupCode' : self.groupCode,
                            'roundCode' : self.roundCode,
                            'seriesCode' : self.seriesCode,
                            'roundOrder' : self.roundOrder }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()

    @classmethod
    def retrieve(cls, game, roundCode, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("""SELECT * FROM gameRound WHERE tournamentCode = (%(tournamentCode)s) 
                        AND roundCode = (%(groundCode)s)
                        AND seriesCode = (%(seriesCode)s)
                        AND groupCode = (%(groupCode)s)""",
                       { 'tournamentCode' : game.series.tournamentCode,
                        'seriesCode' : game.series.seriesCode,
                        'groupCode' : game.groupCode,
                        'roundCode' : roundCode }
                       )
        retorno = cursor.fetchone()
        cursor.close()
        return cls(game, roundCode, retorno['roundorder'])
    
    @classmethod
    def retrieveList(cls, game, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT * FROM gameRound WHERE seriesCode = (%(seriesCode)s)
                        AND tournamentCode = (%(tournamentCode)s)
                        AND groupCode = (%(groupCode)s)""", 
                        {'seriesCode' : game.seriesCode,
                         'tournamentCode' : game.tournamentCode,
                         'groupCode' : game.groupCode}
                        )
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for gameRound in preRetorno:
            retorno.append(GameRound(game, gameRound['roundcode'], gameRound['roundorder']))
        return retorno 
