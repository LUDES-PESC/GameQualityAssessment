# -*- coding: utf-8 -*-
'''
Created on 20/07/2015

@author: mangeli
'''
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import csv

def normalizeData(dados):
    maxPoints= max(dados)
    minPoints= min(dados)
    retorno=[]
    for dado in dados:
        retorno.append((dado-minPoints)/(maxPoints-minPoints))
    return retorno

if __name__ == "__main__":
    arq = csv.reader(open("tabela_resultados_full.csv", "r"))
    tabela = []
    
    for linha in arq:
        tabela.append(linha)
    
    #only data
    pre_dados = []
    edition = []
    for i in xrange(1, len(tabela)):
        edition.append(int(tabela[i][0]))
        pre_dados.append([float(tabela[i][1]), float(tabela[i][2]), float(tabela[i][3])])
    
    dados = np.array(pre_dados)
    #print edition, dados[:,0]
    
    Dpoints = normalizeData(dados[:,0])
    Dposition =normalizeData(dados[:,1])
    Dpath = normalizeData(dados[:,2])
    
    
        
    
    plt.figure()
    y = np.arange(0,1,0.1)
    plt.vlines(edition,0,1,colors='0.75')
    plt.hlines(y, edition[0], edition[-1],colors='0.75')
    
    plt.xlim(edition[0], edition[-1])
    plt.xticks(edition)
    plt.xlabel("Edition")
    plt.ylabel(r'$\frac{Drama(x)-min(Drama)}{max(Drama)-min(Drama)}$', fontsize='large')
    plt.plot(edition, Dpoints, ':ms', markersize=8, linewidth=1.8, label="Drama by points", clip_on=False)
    plt.plot(edition, Dposition, '--r^', markersize=8, linewidth=1.5, label="Drama by position", clip_on=False)
    plt.plot(edition, Dpath, '-bo', markersize=8, linewidth=1.5, label="Drama by path", clip_on=False)
    plt.legend(numpoints=2, fontsize='medium')
    plt.show()
    
    