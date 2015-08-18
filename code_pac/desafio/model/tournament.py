# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''
import psycopg2.extras


class Tournament:
    '''TournamentCode is PK'''
    def __init__(self, tournamentCode, gameName, refYear, country):
        self.tournamentCode = tournamentCode
        self.gameName = gameName
        self.refYear = refYear
        self.country = country

    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Tournament (tournamentCode, gameName, refYear, country)
                           VALUES (%(tournamentCode)s, %(gameName)s, %(refYear)s, %(country)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'gameName' : self.gameName,
                            'refYear' : self.refYear,
                            'country' : self.country }
                            )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
    
    @classmethod
    def retrieve(cls,tournamentCode, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("SELECT * FROM Tournament WHERE tournamentCode = (%s)", (tournamentCode,))
        retorno = cursor.fetchone()
        cursor.close()
        #return cls(retorno[0], retorno[1], retorno[2], retorno[3])
        return cls(retorno['tournamentcode'], retorno['gamename'], retorno['refyear'], retorno['country'])
    
    @classmethod
    def retriveList(cls, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM Tournament")
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for tournament in preRetorno:
            retorno.append(Tournament(tournament['tournamentcode'], tournament['gamename'], tournament['refyear'], tournament['country']))
        return retorno