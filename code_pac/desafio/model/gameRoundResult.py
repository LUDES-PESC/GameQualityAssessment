# -*- coding: utf-8 -*-
'''
Created on 15/05/2015

@author: mangeli
'''
import psycopg2.extras

from gameRound import GameRound
from enrollment import Enrollment
from player import Player


class GameRoundResult:
    '''RoundCode, TournamentCode, SeriesCode, GroupCode, PlayerCode is PK'''
    def __init__(self, gameRound, enrollment, roundScore, totalScore, pRoundStatus):
        if not isinstance(gameRound, GameRound):
            raise TypeError('The firs arg has to be a GameRound object')
        if not isinstance(enrollment, Enrollment):
            raise TypeError('The second arg has to be a Enrollment object')
               
        self.roundCode = gameRound.roundCode
        self.tournamentCode = gameRound.tournamentCode
        self.seriesCode = gameRound.seriesCode
        self.groupCode = gameRound.groupCode
        self.playerCode = enrollment.playerCode
        self.roundScore = roundScore
        self.totalScore = totalScore
        self.pRoundStatus = pRoundStatus
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO GameRoundResult (roundCode, tournamentCode, seriesCode, groupCode, playerCode, roundScore, totalScore, playerRoundStatus)
                           VALUES (%(roundCode)s, %(tournamentCode)s, %(seriesCode)s, %(groupCode)s, %(playerCode)s, %(roundScore)s, %(totalScore)s, %(playerRoundStatus)s)""",
                           {'roundCode' : self.roundCode,
                            'tournamentCode' : self.tournamentCode,
                            'seriesCode' : self.seriesCode,
                            'groupCode' : self.groupCode,
                            'playerCode' : self.playerCode,
                            'roundScore' : self.roundScore,
                            'totalScore' : self.totalScore,
                            'playerRoundStatus' : self.pRoundStatus }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseando-se na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
    @classmethod
    def retrieve(cls, gameRound, enrollment,  connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) # to retrieve a dictionary
        cursor.execute("""SELECT * FROM GameRoundResult WHERE tournamentCode = (%(tournamentCode)s) 
                        AND playerCode = (%(playerCode)s)
                        AND groupCode = (%(groupCode)s)
                        AND seriesCode = (%(seriesCode)s)
                        AND roundCode = (%(roundCode)s)""",
                       { 'tournamentCode' : enrollment.tournamentCode,
                        'playerCode' : enrollment.playerCode,
                        'groupCode' : enrollment.groupCode,
                        'seriesCode' : gameRound.seriesCode,
                        'roundCode' : gameRound.roundCode }
                       )
        retorno = cursor.fetchone()
        cursor.close()
        return cls(gameRound, enrollment, retorno['roundscore'], retorno['totalscore'], retorno['playerroundstatus'])
    
    @classmethod
    def retrieveList(cls, gameRound, connection):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT * FROM GameRoundResult WHERE tournamentCode = (%(tournamentCode)s)
                        AND groupCode = (%(groupCode)s)
                        AND seriesCode =  (%(seriesCode)s)
                        AND roundCode = (%(roundCode)s)""", 
                        {'tournamentCode' : gameRound.tournamentCode,
                         'groupCode' : gameRound.groupCode,
                         'seriesCode' : gameRound.seriesCode,
                         'roundCode' : gameRound.roundCode }
                        )
        preRetorno = cursor.fetchall()
        cursor.close()
        retorno = []
        for roundResult in preRetorno:
            player = Player.retrieve(gameRound.tournament, roundResult['playercode'], connection)
            enrollment = Enrollment.retrieve(player, gameRound.groupCode, gameRound.seriesCode, connection)
            retorno.append(GameRoundResult(gameRound, enrollment, roundResult['roundscore'], roundResult['totalscore'], roundResult['playerroundstatus']))
        return retorno 
