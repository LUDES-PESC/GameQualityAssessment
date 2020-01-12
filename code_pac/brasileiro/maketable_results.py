# -*- coding: utf-8 -*-
'''
Created on 05/07/2015

@author: mangeli
'''
from __future__ import division
from GameQualityAssessment.code_pac.brasileiro.model.game import Game
from GameQualityAssessment.code_pac.model import BrasileiroGame
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import csv, codecs
from io import StringIO
from GameQualityAssessment.project_path import make_absolute_path as abspath
from GameQualityAssessment.code_pac.measures import DramaByPaths, DramaByPositionUp2First, DramaByPointsUp2First

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        #self.writer.writerow([s.encode("utf-8") for s in row])
        self.writer.writerow([s for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        print(data.replace(chr(0),'').replace("\n",""))
        #data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        #data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data.replace(chr(0),'').replace("\n",""))
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':
    #anos = xrange(2003, 2015)
    f = open(abspath('code_pac/brasileiro/tabela_resultados_full.csv'), 'w')
    #f2 = open('tabela_resultados.csv', 'w')
    arq = UnicodeWriter(f)
    arq_r = UnicodeWriter(f)
    fString = '{0:.4f}'
   
    valuesW=[['Edition','Drama by Points', 'Drama by Position', 'Drama by Path']]
    valuesC=[]
    games = Game.retrieveList()
    for game in games:
        genGame = BrasileiroGame(game)
        
        dramaPath = DramaByPaths(game=genGame, ignored=0).getMeasureValue() 
        dramaPoints = DramaByPointsUp2First(game=genGame, ignored=0, normScores=True).getMeasureValue()
        dramaPosition = DramaByPositionUp2First(game=genGame, ignored=0).getMeasureValue()
        
        valuesW.append([game.year, fString.format(dramaPoints), fString.format(dramaPosition), fString.format(dramaPath)])
        valuesC.append([dramaPoints, dramaPosition, dramaPath])
        
    arq.writerows(valuesW)
    f.close()
    #f2.close()
    