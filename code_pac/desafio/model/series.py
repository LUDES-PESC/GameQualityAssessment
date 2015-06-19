# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''
import psycopg2.extras

from tournament import Tournament


class Series:
    '''TournamentCode, SeriesCode is PK'''
    def __init__(self, tournament, seriesCode, seriesOrder):
        if not isinstance(tournament, Tournament):
            raise TypeError('The first arg has to be a Tournament object')
        
        self.tournamentCode = tournament.tournamentCode
        self.seriesCode = seriesCode
        self.seriesOrder = seriesOrder
        self.tournament = tournament
        
    
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Series (tournamentCode, seriesCode, seriesOrder)
                           VALUES (%(tournamentCode)s, %(seriesCode)s, %(seriesOrder)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'seriesCode' : self.seriesCode,
                            'seriesOrder' : self.seriesOrder }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
    
    @classmethod
    def retrieve(cls, tournament, seriesCode, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("""SELECT * FROM Series WHERE tournamentCode = (%(tournamentCode)s) 
                        AND seriesCode = (%(seriesCode)s)""",
                       { 'tournamentCode' : tournament.tournamentCode,
                        'seriesCode' : seriesCode }
                       )
        retorno = cursor.fetchone()
        cursor.close()
        return cls(tournament, seriesCode, retorno['seriesorder'])
    
    @classmethod
    def retrieveList(cls, tournament, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM Series WHERE tournamentCode = (%s)", (tournament.tournamentCode,))
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for series in preRetorno:
            retorno.append(Series(tournament, series['seriescode'], series['seriesorder']))
        return retorno
