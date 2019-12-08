types_list = []
from GameQualityAssessment.code_pac.desafio.model.tournament import Tournament
types_list.append(Tournament)
from GameQualityAssessment.code_pac.desafio.model.player import Player
types_list.append(Player)
from GameQualityAssessment.code_pac.desafio.model.series import Series
types_list.append(Series)
from GameQualityAssessment.code_pac.desafio.model.game import Game
types_list.append(Game)
from GameQualityAssessment.code_pac.desafio.model.gameRound import GameRound
types_list.append(GameRound)
from GameQualityAssessment.code_pac.desafio.model.enrollment import Enrollment
types_list.append(Enrollment)
from GameQualityAssessment.code_pac.desafio.model.gameRoundResult import GameRoundResult
types_list.append(GameRoundResult)

__all__=tuple(types_list)