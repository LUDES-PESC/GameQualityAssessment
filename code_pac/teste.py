'''
Created on 28/05/2015

@author: mangeli
'''
import GameQualityAssessment.code_pac.dataBaseAdapter as db
import os,sys
sys.path.insert(1, os.path.abspath(os.pardir))
print (sys.path)

db.setValues("desafio_simples", "mangeli", "localhost", "agoravai", 5432)
conn = db.getConnection()
c = db.getCursor(conn)
db.cursorExecute(c, "SELECT * FROM tournament;")
l = db.fetchAll(c)
print (l[:])
for retorno in l : print (retorno["country"])
print (c, conn)
db.closeCursor(c)
db.closeConnection(conn)
print (c, conn)





