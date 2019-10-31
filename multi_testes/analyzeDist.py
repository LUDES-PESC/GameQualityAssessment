'''
Created on 11/07/2015

@author: mangeli
'''
from __future__ import division
import math
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook


if __name__ == '__main__':
    wb = load_workbook(filename='envio/dados.xlsx',read_only=True)
    ws = wb['5_r5_t1']
    clean = []
    durty = []
    for row in ws.rows:
        if row[1].value == 1 or row[2].value == 1 or row[3].value == 1 or row[4].value==1:
            durty.append(row[0].value)
        else:
            clean.append(row[0].value)
    print (len(clean), len(durty))
    plt.figure('clean')
    plt.hist(clean)
    plt.xlim((0,1))
    plt.figure('durty')
    plt.hist(durty)
    plt.xlim((0,1))
    plt.show()