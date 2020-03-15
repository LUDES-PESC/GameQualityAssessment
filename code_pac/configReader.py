'''
Created on 05/07/2015

@author: mangeli
'''
import os, configparser
from GameQualityAssessment.project_path import make_absolute_path as abspath

class ConfigReader:
    
    def __init__(self):
        self.parser = configparser.ConfigParser()
        f = open(abspath('code_pac/gameAnalyzer.ini'), 'r')
        self.parser.readfp(f)
        f.close()
    
    def listBrasileiroGames(self):
        r = []
        folder = abspath(self.parser.get('folder brasileiro', 'folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listDiceGames(self):
        r = []
        folder = abspath(self.parser.get('folder dado', 'folder'))
        for f in os.listdir(folder):
            r.append(folder + os.sep + f)
        return r
    
    def listPremierLeagueGames(self):
        r = []
        folder = abspath(self.parser.get('folder ingles','folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listLaLigaGames(self):
        r = []
        folder = abspath(self.parser.get('folder espanhol','folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listLegaNazionaleGames(self):
        r = []
        folder = abspath(self.parser.get('folder italiano','folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listBunsligaGames(self):
        r = []
        folder = abspath(self.parser.get('folder alemao','folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listPrimeiraLigaGames(self):
        r = []
        folder = abspath(self.parser.get('folder portugal','folder'))
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listPontosCorridosGames(self):
        r = []
        countries = ['brasileiro','ingles','espanhol','italiano','alemao','portugal']
        for country in countries:
            folder = abspath(self.parser.get('folder '+country,'folder'))
            for f in os.listdir(folder):
                if f.startswith("simples"):
                    r.append(folder + os.sep + f)
        return r
        

if __name__ == '__main__':
    c = ConfigReader()
    print (c.listBrasileiroGames())