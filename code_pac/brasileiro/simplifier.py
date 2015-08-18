# -*- coding: utf-8 -*-
'''
Created on 13/07/2015

@author: mangeli
'''
from __future__ import division

from bs4 import BeautifulSoup
from openpyxl import Workbook

#<div class="rodada-tabela">
#<tr class="linha-classificacao" rel="juventude" data-escudo="http://s.glbimg.com/es/sde/f/organizacoes/2011/01/03/juventude30.png">


if __name__ == '__main__':
    anos = range(2003, 2015)
    wb = Workbook()
    for ano in anos:
        entrada = open('../../data/brasileiro/raw_data/full' + str(ano), 'r')
        planilha = wb.create_sheet(title=str(ano))
        planilha.append(['rodada', u'posição', 'equipe', 'pontos', 'jogos', u'vitórias', 'empates', 'derrotas', 'gols pro', 'gols contra', 'saldo', 'aproveitamento'])
        parser = BeautifulSoup(entrada.read())
        entrada.close()
        rodadas = parser.find_all('div','rodada-tabela')
        for rodada in rodadas:
            numRodada = rodada.find('table', class_='tabela')['data-rodada']
            for linha in rodada.find_all('tr', 'linha-classificacao'):
                dados = [int(numRodada),
                         int(linha.find('td', rel='grafico-posicao').find_next().text),
                         linha.find('td','time').text.strip(),
                         int(linha.find('td', rel='jogos-pontos').find_next().text),
                         int(linha.find('td', rel='jogos-jogos').find_next().text),
                         int(linha.find('td', rel='jogos-vitorias').find_next().text),
                         int(linha.find('td', rel='jogos-empates').find_next().text),
                         int(linha.find('td', rel='jogos-derrotas').find_next().text),
                         int(linha.find('td', rel='gols-pro').find_next().text),
                         int(linha.find('td', rel='gols-contra').find_next().text),
                         int(linha.find('td', rel='grafico-saldo').find_next().text),
                         float(linha.find('td', rel='grafico-aproveitamento').find_next().text)
                         ]
                planilha.append(dados)
                #print dados
    wb.save('../../data/brasileiro/raw_data/dados.xlsx')