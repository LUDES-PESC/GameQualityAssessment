# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''
import psycopg2.extras

from series import Series
import code_pac.measures


class Game:
    '''Tournament, SeriesCode, GroupCode is PK'''
    def __init__(self, series, groupCode):
        if not isinstance(series, Series):
            raise TypeError('The first arg has to be a Series object')
        
        self.tournamentCode = series.tournamentCode
        self.seriesCode = series.seriesCode
        self.groupCode = groupCode
        self.series = series
        self.tournament = series.tournament
        
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Game (tournamentCode, seriesCode, groupCode)
                           VALUES (%(tournamentCode)s, %(seriesCode)s, %(groupCode)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'seriesCode' : self.seriesCode,
                            'groupCode' : self.groupCode }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
    
    def storeMeasure(self, measureIn, connection):
        if not isinstance(measureIn, code_pac.measures.MeasureTemplate):
            raise TypeError("First arg has to be a MeasureTemplate implementer object")
        
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO measures (tournamentCode, seriesCode, groupCode, 
                                measureCode, measureDescription, measureVersion, measureValue)
                           VALUES (%(tournamentCode)s, %(seriesCode)s, %(groupCode)s, 
                           %(measureCode)s, %(measureDescription)s, %(measureVersion)s, %(measureValue)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'seriesCode' : self.seriesCode,
                            'groupCode' : self.groupCode,
                            'measureCode' : measureIn.getType().code,
                            'measureDescription' : measureIn.getType().description,
                            'measureVersion' : measureIn.getType().version,
                            'measureValue' : measureIn.getMeasureValue() }
                           )
        except psycopg2.Error: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
    
    def retrieveMeasureList(self, connection, versions="last"):
        '''
        versions=last (default) returns the last version of all measures
        versions=all returns all version of all measures
        '''
        complStr = ""
        if versions == "last":
            complStr = """ AND measureVersion = (SELECT max(measureVersion) from measures as M2
                            WHERE M2.tournamentCode = M.tournamentCode
                            AND M2.seriesCode = M.seriesCode
                            AND M2.groupCode = M.groupCode
                            AND M2.measureCode = M.measureCode) """
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT * FROM measures as M 
                        WHERE seriesCode = %(seriesCode)s 
                        AND tournamentCode = %(tournamentCode)s 
                        AND groupCode = %(groupCode)s""" + complStr,
                        {'seriesCode' : self.seriesCode,
                         'tournamentCode' : self.tournamentCode,
                         'groupCode' : self.groupCode
                         })
        retorno = cursor.fetchall()
        cursor.close()
        return retorno
       
    @classmethod
    def retrieveList(cls, series, connection):
        if not isinstance(series, Series):
            raise TypeError('The first arg has to be a Series object')
        
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT * FROM Game WHERE seriesCode = (%(seriesCode)s)
                        AND tournamentCode = (%(tournamentCode)s)""", 
                        {'seriesCode' : series.seriesCode,
                         'tournamentCode' : series.tournament.tournamentCode}
                        )
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for game in preRetorno:
            retorno.append(Game(series, game['groupcode']))
        return retorno
