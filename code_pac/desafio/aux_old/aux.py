# -*- coding: utf-8 -*-
from __future__ import division

import Parser


#abre o arqruivo
parser = Parser('/home/mangeli/Dropbox/mestrado/dados desafio sebrae/Pontuação2.xlsx')

#le o arquivo
linhas = parser.getValues(0, 0) #planilha 0 com zero linhas de cabecalho

tamanho = []
for i in linhas[0]:
    tamanho.append(0)

for i in range(len(linhas)):
    for j in range(len(linhas[i])):
        if not isinstance(linhas[i][j], (float, int, long)):
            if len(linhas[i][j]) > tamanho[j]:
                tamanho[j] = len(linhas[i][j])
        else:
            if tamanho[j] == 0:
                tamanho[j] = str(type(linhas[i][j])) 
    print str((i / len(linhas) * 100)), "%", "                      \r",

print ""

print tamanho