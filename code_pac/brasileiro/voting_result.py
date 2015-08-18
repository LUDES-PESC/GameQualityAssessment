'''
Created on 23/07/2015

@author: mangeli
'''
from __future__ import division
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from pyvotecore.schulze_pr import SchulzePR
from pyvotecore.schulze_method import SchulzeMethod
from pyvotecore.schulze_npr import SchulzeNPR


def assignValues(row, limit=None):
    if limit == None:
        limit = len(row)
    retorno = []
    editions = xrange(2003, 2014+1)
    for i in xrange(1, limit):
                retorno.append(row[i].value-1)
    return [[str(x)] for(y,x) in sorted(zip(retorno, editions))]#retorno

if __name__ == '__main__':
    wb = load_workbook(filename='ranking.xlsx',read_only=True)
    ws = wb['Planilha1']
    
    ballots = []
    for row in ws.rows:
        if row[0].value == "x":
            cedula = assignValues(row, 13)
            ballots.append({"count":1, "ballot":cedula}) 
    #r = SchulzePR(ballots).as_dict()
    print ballots
    #print SchulzeMethod(ballots, ballot_notation=0).as_dict()
    #print SchulzePR(ballots, ballot_notation=0).as_dict()['order']
    print SchulzeNPR(ballots, ballot_notation=0).as_dict()['order']