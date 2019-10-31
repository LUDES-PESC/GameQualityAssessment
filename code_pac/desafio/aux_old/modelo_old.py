# -*- coding: utf-8 -*-
import psycopg2
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
            connection.rollback()       # baseandose na chave primária da tabela
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

class Series:
    '''TournamentCode, SeriesCode is PK'''
    def __init__(self, tournament, seriesCode, seriesOrder):
        if not isinstance(tournament, Tournament):
            raise TypeError('The first arg has to be a Tournament object')
        
        self.tournamentCode = tournament.tournamentCode
        self.seriesCode = seriesCode
        self.seriesOrder = seriesOrder
    
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
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
        
class PlayerGroup:
    '''GroupeCode, TournamentCode is PK'''
    def __init__(self, tournament, groupCode):
        if not isinstance(tournament, Tournament):
            raise TypeError('The first arg has to be a Tournament object')
        
        self.groupCode = groupCode
        self.tournamentCode = tournament.tournamentCode
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO PlayerGroup (tournamentCode, groupCode)
                           VALUES (%(tournamentCode)s, %(groupCode)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'groupCode' : self.groupCode }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
class Game:
    '''Tournament, SeriesCode, GroupCode is PK'''
    def __init__(self, series, playerGroup):
        if not isinstance(series, Series) or not isinstance(playerGroup, PlayerGroup):
            raise TypeError('First arg has to be a Series object. Second arg has to be a PlayerGroup object')
        
        self.tournamentCode = series.tournamentCode
        self.seriesCode = series.seriesCode
        self.groupCode = playerGroup.groupCode
        
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
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
class Enrollment:
    '''GroupCode, TournamentCode, PlayerCode is PK'''
    
    def __init__(self, player, playerGroup, finalScore):
        if not isinstance(player, Player):
            raise TypeError('The first arg has to be a Player object')
        if not isinstance(playerGroup, PlayerGroup):
            raise TypeError('The second arg has to be a PlayerGroup object')
        
        
        self.groupCode = playerGroup.groupCode
        self.playerCode = player.playerCode
        self.tournamentCode = player.tournamentCode
        self.finalScore = finalScore
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Enrollment (groupCode, tournamentCode, playerCode, finalScore)
                           VALUES (%(groupCode)s, %(tournamentCode)s, %(playerCode)s, %(finalScore)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'groupCode' : self.groupCode,
                            'playerCode' : self.playerCode,
                            'finalScore' : self.finalScore}
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
class GameRound:
    '''RoundCode, TournamentCode, SeriesCode, GroupCode is PK'''
  
    def __init__(self, game, roundCode, roundNumber):
        if not isinstance(game, Game):
            raise TypeError('The first arg has to be a Game object')
        
        self.roundCode = roundCode
        self.tournamentCode = game.tournamentCode
        self.seriesCode = game.seriesCode
        self.groupCode = game.groupCode
        self.roundNumber = roundNumber
        
    def store(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""INSERT INTO Round (roundCode, tournamentCode, seriesCode, groupCode, roundNumber)
                           VALUES (%(roundCode)s, %(tournamentCode)s, %(seriesCode)s, %(groupCode)s, %(roundNumber)s)""",
                           {'tournamentCode' : self.tournamentCode,
                            'groupCode' : self.groupCode,
                            'roundCode' : self.roundCode,
                            'seriesCode' : self.seriesCode,
                            'roundNumber' : self.roundNumber }
                           )
        except psycopg2.IntegrityError: # simula um insert ignore, não insere dados que já existem
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()
        
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
            connection.rollback()       # baseandose na chave primária da tabela
        else:
            connection.commit()
        cursor.close()