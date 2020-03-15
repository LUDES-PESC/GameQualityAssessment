'''
Created on 27/05/2015
FIXME
@author: mangeli
'''
from __future__ import division

from bs4 import BeautifulSoup
import json
from GameQualityAssessment.project_path import make_absolute_path as abspath


#anos = range(2003, 2014)
anos = ['2013-2013', '2014']

def montaRanking(tabelaDados):
    #pegando o ranking da rodada
    ranking = []
    for linha in tabelaDados.find_all('tr', 'linha-classificacao'):
        ranking.append([linha.find('td','time').text.strip(), int(linha.find('td', rel='jogos-pontos').find_next().text)])
    return ranking



for ano in anos:
    campeonato = []
    file_to_be_open = 'data/raw_data/full' + str(ano)
    entrada = open(abspath(file_to_be_open), 'r')
    parser = BeautifulSoup(entrada.read())
    entrada.close()
    
    saida = open(abspath('data/raw_data/simples_' + str(ano)), 'w')    
    rodadas = parser.find_all('div','rodada-tabela')
    print (ano, len(rodadas))
    for rodada in rodadas:
        campeonato.append(montaRanking(rodada))
    #print '          \r', rodada.find_next().get('data-rodada'), " ", int(rodada.text) / len(rodadas) * 100, '%'
    json.dump(campeonato, saida)
    saida.close()
    
    

    
