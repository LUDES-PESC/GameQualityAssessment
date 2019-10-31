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
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':
    anos = range(2003, 2015)
    f = open('tabela_resultados_full.csv', 'w')
    f2 = open('tabela_resultados.csv', 'w')
    arq = UnicodeWriter(f)
    arq_r = UnicodeWriter(f)
    
    header = ['Edition','Teams No.', 'Rounds No.', 'Winner', 'Winner final score', 'Winner effectiveness']
    for ano in anos:
        entrada = open('../../data/brasileiro/raw_data/full' + str(ano), 'r')
        parser = BeautifulSoup(entrada.read())
        entrada.close()
        rodadas = parser.find_all('div','rodada-tabela')
        #contando rodadas
        nRodadas = len(rodadas)
        #get last rodada
        ultimaRodada = rodadas[nRodadas-1]
        #times
        times = ultimaRodada.find_all('tr', 'linha-classificacao')
        nTimes = str(len(times))
        vencedor = times[0].find('td','time').text.strip()
        if not int(times[0].find('td', rel='grafico-posicao').find_next().text) == 1:
            raise Exception('Primeiro da lista não tem primeira posição:' + ano)
        scoreVencedor = times[0].find('td', rel='jogos-pontos').find_next().text
        aproveitamento = times[0].find('td', rel='grafico-aproveitamento').find_next().text
        arq.writerow([ str(ano), nTimes, str(nRodadas), vencedor, scoreVencedor, aproveitamento])
        print (ano, nTimes, nRodadas, vencedor, scoreVencedor, aproveitamento)
    