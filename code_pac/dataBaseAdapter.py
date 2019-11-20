# -*- coding: utf-8 -*-
'''
Created on 24/05/2015

@author: mangeli
'''
import configparser
import psycopg2.extras
import os


__dbname = None #desafio_simples
__user = None #mangeli
__host = None #localhost
__password = None #agoravai
__port = None #5432


def setValues(dbname, user, host, password, port):
    global __dbname
    global __user
    global __host
    global __password
    global __port
    __dbname = dbname
    __user = user
    __host = host
    __password = password
    __port = port


def getConfigValues():
    global __dbname
    global __user
    global __host
    global __password
    global __port
    conf_parser = configparser.ConfigParser()
    f = open(os.path.dirname(__file__) + '//gameAnalyzer.ini', 'r')
    conf_parser.read_file(f)
    f.close()
    
    __dbname = conf_parser.get('database desafio', 'dbname')
    __user = conf_parser.get('database server', 'user')
    __host = conf_parser.get('database server', 'host')
    __password = conf_parser.get('database server', 'password')
    __port = conf_parser.get('database server', 'port')


def getConnection():
    global __dbname
    global __user
    global __host
    global __password
    global __port
    
    
    
    if __dbname == None or __user == None or __host == None or __password == None:
        getConfigValues() #try read data from ini file
    
    if __dbname == None or __user == None or __host == None or __password == None:    
        raise Exception("Database configuration error. Try use the 'setValues' function.")
    
    return psycopg2.connect("dbname=" + __dbname + " user=" + __user + " host=" + __host + " password=" + __password + " port=" + str(__port))

def getCursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def cursorExecute(c, sql):
    c.execute(sql)

def fetchOne(c):
    return c.fetchone()

def fetchAll(c):
    return c.fetchall()
    
def closeCursor(c):
    c.close()
    
def closeConnection(conn):
    conn.close()

if __name__ == "__main__":
    #setValues("desafio_simples", "mangeli", "localhost", "agoravai", 5432)
    conn = getConnection()
    c = getCursor(conn)
    cursorExecute(c, "SELECT * FROM tournament;")
    l = fetchAll(c)
    print (l[:])
    for retorno in l : print (retorno["country"])
    print (c, conn)
    closeCursor(c)
    closeConnection(conn)
    print (c, conn)