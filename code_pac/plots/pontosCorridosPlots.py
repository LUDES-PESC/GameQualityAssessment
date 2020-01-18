import matplotlib
import numpy
from GameQualityAssessment.code_pac.model import PontosCorridosGame

def points(inputGame, panel, ignored=0):
    obj = PontosCorridosGame(inputGame)
    players = obj.getPlayers()
    gameObj = obj.getGameStruct()
    panel.figure.clf()
    graphical = panel.figure.gca()

    len_gameRounds = obj.getNumberRounds()
    for player in players:
        x = list(range(1+ignored,len_gameRounds+1))
        y = []
        for index in range(0+ignored,len_gameRounds):
            round = obj.getRound(index+1)
            for item_tuple in round[1]:
                if item_tuple.playerCode == player:
                    y.append(item_tuple.totalScore)
            pass
        graphical.plot(x,y,'o-',lineWidth=2)
        #print(player,y,"<----")
    graphical.set_ylabel('Points')
    graphical.set_xlabel('Round')
    panel.draw()
    

def positions(inputGame, panel, ignored=0):
    obj = PontosCorridosGame(inputGame)
    players = obj.getPlayers()
    gameObj = obj.getGameStruct()
    panel.figure.clf()
    graphical = panel.figure.gca()

    len_gameRounds = obj.getNumberRounds()
    for player in players:
        x = list(range(1+ignored,len_gameRounds+1))
        y = []
        for index in range(0+ignored,len_gameRounds):
            round = obj.getRound(index+1)
            count = 0
            for item_tuple in round[1]:
                count = count + 1
                if item_tuple.playerCode == player:
                    y.append(count)
            pass
        graphical.plot(x,y,'o-',lineWidth=2)
        #print(player,y,"<----")

    graphical.set_yticks(list(range(0,len(players)+1)))
    graphical.set_ylabel("Position")
    graphical.set_xlabel("Round")
    graphical.invert_yaxis()
    panel.draw()

def values_histogram(values,panel,label=''):
    panel.figure.clf()
    graphical = panel.figure.gca()
    graphical.hist(values,bins=20,rwidth=0.9,range=(0,1), zorder=2)
    graphical.set_xlabel(label)
    panel.draw()
