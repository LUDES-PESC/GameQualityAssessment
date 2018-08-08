'''
Created on 05/07/2015

@author: mangeli
'''
import os, ConfigParser

class ConfigReader:
    
    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        f = open(os.path.dirname(__file__) + '//gameAnalyzer.ini', 'r')
        self.parser.readfp(f)
        f.close()
    
    def listBrasileiroGames(self):
        r = [];
        folder = os.path.dirname(__file__) + os.sep + self.parser.get('folder brasileiro', 'folder')
        for f in os.listdir(folder):
            if f.startswith("simples"):
                r.append(folder + os.sep + f)
        return r
    
    def listDiceGames(self):
        r = [];
        print os.path.dirname(__file__);
        print os.sep
        print self.parser.get('folder dado', 'folder')
        folder = os.path.dirname(__file__) + os.sep + self.parser.get('folder dado', 'folder')
        for f in os.listdir(folder):
            r.append(folder + os.sep + f)
        return r
        

if __name__ == '__main__':
    c = ConfigReader();
    print c.listBrasileiroGames()