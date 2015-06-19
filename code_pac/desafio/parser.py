# -*- coding: utf-8 -*-

import xlrd


#'/home/mangeli/Dropbox/mestrado/dados desafio sebrae/Pontuação2.xlsx', encoding_override='8859-1'
class Parser:
    def __init__(self, arquivo):
        self.openFile(arquivo)
    def openFile(self, arquivo):
        self.workbook = xlrd.open_workbook(arquivo)
    def getWorksheet(self, indice):
        self.worksheet = self.workbook.sheet_by_index(indice)
    def getValues(self, worksheetIndex, headerLines):
        self.getWorksheet(worksheetIndex)
        offset = headerLines # use -1 to no headers rows
        rows = []
        for i, row in enumerate(range(self.worksheet.nrows)):
            if i <= offset:  # (Optionally) skip headers
                continue
            r = []
            for j, col in enumerate(range(self.worksheet.ncols)):
                r.append(self.worksheet.cell_value(i, j))
                '''if isinstance(r, unicode):
                r = r.encode('utf8')
                print ('sim') '''
            rows.append(r)
        return rows
    
'''    
parser = Parser('/home/mangeli/Dropbox/mestrado/dados desafio sebrae/Pontuação2.xlsx')
cabecalho = -1 # nenhuma linha de cabeçalho
rows = parser.getValues(0, cabecalho)
print 'Got ' + str(len(rows) - cabecalho) + ' rows' 
print rows[0]  # Print column headings
print rows[cabecalho]  # Print first data row sample
'''

        
        

