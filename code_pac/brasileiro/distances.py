'''
Created on 22/07/2015

@author: mangeli
'''
from __future__ import division
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
import scipy.stats
import scipy.spatial.distance

def assignValues(row):
    retorno = []
    for i in range(0, len(row)):
                retorno.append(row[i].value)
    return retorno

if __name__ == '__main__':
    wb = load_workbook(filename='vetores.xlsx',read_only=True)
    ws = wb['Sheet1']
    path = []
    points =[]
    positions = []
    judges = []
    for row in ws.rows:
        if row[0].value == "path":
            path = assignValues(row)
        if row[0].value == "points":
            points = assignValues(row)   
        if row[0].value == "positions":
            positions = assignValues(row)  
        if row[0].value == "judges":
            judges = assignValues(row)
    
    print (scipy.stats.kendalltau(judges, points))
    print (scipy.stats.kendalltau(judges, positions))
    print (scipy.stats.kendalltau(judges, path))
    print (scipy.spatial.distance.hamming(judges, points))  
    print (scipy.spatial.distance.hamming(judges, path))  
    print (scipy.spatial.distance.cosine(judges, points))  
    print (scipy.spatial.distance.cosine(judges, path))
    print (scipy.spatial.distance.correlation(judges, points))  
    print (scipy.spatial.distance.correlation(judges, path))
              
            