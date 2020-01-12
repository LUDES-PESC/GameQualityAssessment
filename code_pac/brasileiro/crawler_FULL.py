'''
Created on 28/05/2015

@author: mangeli
'''
import requests
from GameQualityAssessment.project_path import make_absolute_path as abspath

#for ano in xrange(2003, 2014):
for ano in ['2013-2013', '2014']:
    f = open(abspath('../data/raw_data/full' + str(ano)), 'w')
    f.write(requests.get('http://futpedia.globo.com/campeonato/campeonato-brasileiro/' + ano).text.encode('utf-8'))
    f.close()

