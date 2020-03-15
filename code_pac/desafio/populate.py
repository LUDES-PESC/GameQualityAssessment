# -*- coding: utf-8 -*-
from __future__ import division



from GameQualityAssessment.code_pac import dataBaseAdapter as db
from multiprocessing import Pool, Process, Value, Lock, Array
from GameQualityAssessment.code_pac.desafio.parser import Parser
from GameQualityAssessment.project_path import make_absolute_path as abspath
import GameQualityAssessment.code_pac.desafio.model as model

MAX_BUFFER = 8

def procDataLines(dataLine,contador, tamanho, l):
    #db.setValues('desafio_simples', 'mangeli', 'localhost', 'agoravai', 5432)
    conn = db.getConnection() 
    
    tournament = model.Tournament(int(dataLine[5]), dataLine[2], int(dataLine[1]), dataLine[0])
    tournament.store(conn)
    
    player = model.Player(tournament, int(dataLine[8]), dataLine[14], dataLine[13], dataLine[16])
    player.store(conn)
    
    series = model.Series(tournament, int(dataLine[6]), int(dataLine[3]))
    series.store(conn)
    
    game = model.Game(series, int(dataLine[7]))
    game.store(conn)
    
    enrollment = model.Enrollment(player, int(dataLine[7]), int(dataLine[6]), dataLine[20])
    enrollment.store(conn)
    
    gameRound = model.GameRound(game, int(dataLine[9]), int(dataLine[4]))
    gameRound.store(conn)
    
    
    roundResult = model.GameRoundResult(gameRound, enrollment, dataLine[18], dataLine[19], dataLine[11])
    roundResult.store(conn)
    
    with contador.get_lock():
        contador.value += 1
    l.acquire()
    #print str((contador.value / tamanho.value) * 100), " %", "                                \r",
    l.release()
    conn.close()

def consumidor(buffer,index,quantity,contador,tamanho,l,runmethod):
    while(True):
        wait = True
        while(wait):
            if(contador.value >= tamanho.value): return
            with quantity.get_lock():
                if(quantity.value > 0):
                    wait = False
        l.acquire()
        index.value = (index.value + 1) % MAX_BUFFER
        dataLine = buffer[index.value].it
        quantity.value = quantity.value - 1
        l.release()
        runmethod(dataLine,contador,tamanho,l)

def produtor(feed,buffer,index,quantity,contador,tamanho,l):
    for line in feed:
        wait = True
        while(wait):
            with quantity.get_lock():
                if(quantity.value < MAX_BUFFER):
                    wait = False
        l.acquire()
        index.value = (index.value + 1) % MAX_BUFFER
        buffer[index.value].it = line
        quantity.value = quantity.value + 1
        l.release()

class myList:
    it = [ ]
    def __len__(self):
        import sys
        return sys.getsizeof(myList)



if __name__ == "__main__":

    #abre o arqruivo
    print("Abrindo dados.xlsx ....")
    parser = Parser(abspath('data/desafio/raw_data/dados.xlsx')) 
    print("Planilha carregada")
    #le o arquivo
    linhas = parser.getValues(0, 0) #planilha 0 com zero linhas de cabecalho
    #linhas = []
    print("Número de linhas da planilha:")
    print (len(linhas))
    #imprime a associacao entre índice e nome do campo
    #for i in range(len(linhas[0])):
    #    print str(i) + ' - ' + linhas[0][i]
    
    #for i in linhas:
    #    print i
        
    #for i in range(len(linhas)):
    #    print "linha ", str(i+1), " de ", str(len(linhas)) + "\r",
    
    print("Criando variáveis")
    #buff = Array(myList, 8)
    #quant = Value('i',0)
    #begin = Value('i',0)
    #end = Value('i',0)
    contador = Value('i', 0)
    tamanho = Value('i', len(linhas))
    l=Lock()
    #pool = Pool(processes=4)
    #pool.map(procDataLines, (linhas))
    #pool.close()
    #pool.join()
    print("Começando processamento")
    #feeder = Process(target=produtor,args=(linhas,buff,end,quant,contador,tamanho,l,))
    #process = Process(target=consumidor,args=(buff,begin,quant,contador,tamanho,l,procDataLines,))
    #process.start()
    #process.join()
    cont = 0.0
    numLinhas = len(linhas)*1.0
    NUMBER_OF_LINES = len(linhas)
    for index in range(0,NUMBER_OF_LINES,8) :
        process1 = Process(target=procDataLines,args=(linhas[index],contador,tamanho,l,))
        if(index+1 < numLinhas): process2 = Process(target=procDataLines,args=(linhas[index+1],contador,tamanho,l,))
        if(index+2 < numLinhas): process3 = Process(target=procDataLines,args=(linhas[index+2],contador,tamanho,l,))
        if(index+3 < numLinhas): process4 = Process(target=procDataLines,args=(linhas[index+3],contador,tamanho,l,))
        if(index+4 < numLinhas): process5 = Process(target=procDataLines,args=(linhas[index+4],contador,tamanho,l,))
        if(index+5 < numLinhas): process6 = Process(target=procDataLines,args=(linhas[index+5],contador,tamanho,l,))
        if(index+6 < numLinhas): process7 = Process(target=procDataLines,args=(linhas[index+6],contador,tamanho,l,))
        if(index+7 < numLinhas): process8 = Process(target=procDataLines,args=(linhas[index+7],contador,tamanho,l,))
        process1.start()
        if(index+1 < numLinhas): process2.start()
        if(index+2 < numLinhas): process3.start()
        if(index+3 < numLinhas): process4.start()
        if(index+4 < numLinhas): process5.start()
        if(index+5 < numLinhas): process6.start()
        if(index+6 < numLinhas): process7.start()
        if(index+7 < numLinhas): process8.start()
        process1.join()
        if(index+1 < numLinhas): process2.join()
        if(index+2 < numLinhas): process3.join()
        if(index+3 < numLinhas): process4.join()
        if(index+4 < numLinhas): process5.join()
        if(index+5 < numLinhas): process6.join()
        if(index+6 < numLinhas): process7.join()
        if(index+7 < numLinhas): process8.join()
        cont = cont+8.0
        print(cont/numLinhas)
    print ("Fim do processamento")
    '''print linhas[0][:]
    procDataLines(linhas[0])'''
