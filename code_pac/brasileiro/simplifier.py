# -*- coding: utf-8 -*-
'''
Created on 13/07/2015

@author: mangeli
'''
from __future__ import division

from bs4 import BeautifulSoup
from openpyxl import Workbook
from GameQualityAssessment.project_path import make_absolute_path as abspath

#<div class="rodada-tabela">
#<tr class="linha-classificacao" rel="juventude" data-escudo="http://s.glbimg.com/es/sde/f/organizacoes/2011/01/03/juventude30.png">


if __name__ == '__main__':
    anos = range(2003, 2015)
    wb = Workbook()
    for ano in anos:
        print("Carregando arquivo do ano "+str(ano))
        entrada = open(abspath('data/brasileiro/raw_data/full' + str(ano)), 'r')
        planilha = wb.create_sheet(title=str(ano))
        planilha.append(['rodada', 'posição', 'equipe', 'pontos', 'jogos', 'vitórias', 'empates', 'derrotas', 'gols pro', 'gols contra', 'saldo', 'aproveitamento'])
        print("Carregando BeatifulSoup")
        parser = BeautifulSoup(entrada.read(), features="html.parser")
        entrada.close()
        print("Realizando busca...")
        rodadas = parser.find_all('div','rodada-tabela')
        print("Número de rodadas encontradas: ", str(len(rodadas)) )
        print("Escrevendo dados a planilha...")
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
    wb.remove(wb.worksheets[0])
    print("Número de planilhas geradas: "+str(len(wb.worksheets)))
    wb.save(abspath('data/brasileiro/raw_data/dados.xlsx'))