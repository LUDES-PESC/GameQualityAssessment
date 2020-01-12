# -*- coding: utf-8 -*-
'''
Created on 13/07/2015

@author: mangeli
'''
from __future__ import division

from bs4 import BeautifulSoup
from openpyxl import Workbook
import datetime
from GameQualityAssessment.project_path import make_absolute_path as abspath

#<div class="rodada-tabela">
#<tr class="linha-classificacao" rel="juventude" data-escudo="http://s.glbimg.com/es/sde/f/organizacoes/2011/01/03/juventude30.png">


if __name__ == '__main__':
    anos = range(2003, 2015)
    wb = Workbook()
    for ano in anos:
        entrada = open(abspath('data/brasileiro/raw_data/full') + str(ano), 'r')
        planilha = wb.create_sheet(title=str(ano))
        planilha.append(['rodada', 'data-hora', 'local', 'mandante', 'gols-mandante', 'gols-visitante', 'visitante'])
        parser = BeautifulSoup(entrada.read())
        entrada.close()
        rodadas = parser.find_all('div',id='lista-jogos')
        for rodada in rodadas:
            
            
            for linha in rodada.find_all('li', class_='lista-classificacao-jogo'):
                numRodada = linha['data-rodada']
                dia = linha.find('time', itemprop='startDate')['datetime'].split('/')
                hora = linha.find('div', class_='data-local').find('span', class_='horario').text.split('h')
                dados = [int(numRodada),
                        datetime.datetime(int(dia[2]), int(dia[1]), int(dia[0]), int(hora[0]), int(hora[1])),
                        linha.find('div', class_='data-local').find('span', itemprop='name').text,
                        linha.find('div', class_='info-jogo').find('div', class_='mandante').find('meta')['content'],
                        int(linha.find('div', class_='info-jogo').find('div', class_='placar').find('span', class_='mandante').text),
                        int(linha.find('div', class_='info-jogo').find('div', class_='placar').find('span', class_='visitante').text),
                        linha.find('div', class_='info-jogo').find('div', class_='visitante').find('meta')['content']
                         ]
                planilha.append(dados)
                #print dados
    wb.save( abspath('data/brasileiro/raw_data/jogos_dados.xlsx') )