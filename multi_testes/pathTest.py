# -*- coding: utf-8 -*-
'''
Created on 08/07/2015

@author: mangeli
'''
from __future__ import division
import math


def maxDrama(nPlayers, nRounds, gRound, target=1):
        x1 = 1 #primeira rodada 
        y1 = nPlayers #na última posição
        x2 = nRounds #última rodada
        y2 = target #primeira posição
        return math.ceil(  (y2-y1)*(gRound-x1)/(x2-x1) + y1 )

def pathDrama(path, nPlayers, target=1):
    weakCount = 0
    distSum = 0
    for index in xrange(len(path)):
        diff = abs(path[index] - maxDrama(nPlayers, len(path), index+1, target))
        distSum += diff / ((nPlayers - 1) * (len(path)- 1))
        if path[index] > target:
            weakCount += 1
    return (weakCount / (len(path) - 1)) *(1 - (distSum))
    #return 1-distSum

def pathMaker(nPlayers, nRounds, target = 1):
    path = []
    while len(path) < nPlayers**(nRounds - 1): #TODO ultima rodada é sempre o alvo
        path = putPlayer(nPlayers, path)
    for p in xrange(len(path)):
        path[p] += [target]
    return path

def putPlayer(nPlayers, paths):
    listPaths = paths[:]
    newPaths = []    
    if len(paths) == 0: #primeira rodada
        for p in xrange(1, nPlayers + 1):
            newPaths.append([p])
    else:
        while len(listPaths) > 0:
            sub = listPaths.pop()
            for pos in xrange(1, nPlayers + 1):
                newPaths.append(sub + [pos])
    return newPaths



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from openpyxl import Workbook
    
    wb = Workbook()
    
    for players in xrange(3,7):
        for gRounds in xrange(3,9):
            for target in xrange(1,5):
                if target > players - 1:
                    break
                identiS = str(players) + '_r' + str(gRounds) + '_t' + str(target)
                pp = PdfPages('envio/graficos_p' + identiS + '.pdf')
                planilha = wb.create_sheet(title=identiS)
                paths = pathMaker(players, gRounds, target)
                values = []
                for path in paths:
                    #print path
                    drama = pathDrama(path, players, target)
                    values.append(drama)
                    planilha.append([drama]+path)
                values = sorted(values)
                #print values[:]
                titleGr = 'Players=' + str(players) + " | Rounds=" + str(gRounds) + " | target=" + str(target)
                plt.figure()
                plt.title(titleGr)
                #plt.subplot(131)
                plt.hist(values, bins=10)
                pp.savefig()
                plt.close()
                
                plt.figure()
                plt.title(titleGr)
                #plt.subplot(132)
                plt.plot(values, 'ro')
                '''for path in paths: 
                    plt.figure()
                    plt.plot(path)'''
                pp.savefig()
                plt.close()
                
                MDP=[]
                for x in xrange(1, gRounds + 1):
                    MDP.append(maxDrama(players, gRounds, x, target))
                #plt.subplot(133)
                plt.figure()
                plt.title(titleGr)
                plt.plot(MDP, 'r-o')
                plt.ylim(1,players)
                plt.yticks(xrange(1,players + 1))
                plt.gca().invert_yaxis()
                pp.savefig()
                plt.close()
                pp.close()
    wb.save('envio/dados.xlsx')
    #plt.show()