import GameQualityAssessment.code_pac.configReader as configReader
from GameQualityAssessment.project_path import make_absolute_path as abspath
import csv
import os

def get_players(open_csv):
    ps = []
    mrc = {}
    for line in open_csv:
        row = line[0].split(';')
        if row[0] == "E0":
            p1 = r""+row[2]
            p2 = r""+row[3]
            if mrc.get(p1,None) == None : ps.append(p1)
            if mrc.get(p2,None) == None : ps.append(p2) 
            mrc[p1] = 0
            mrc[p2] = 0
    return ps

def make_map_player_index(players):
    player_index = {}
    for i in range(0,len(players)):
        player_index[players[i]] = i
    return player_index
    

def make_round(prev_round,players):
    placar = [[players[i],0] for i in range(0,len(players))]
    if prev_round != None:
        for i in range(0,len(players)):
            placar[i][1] = placar[i][1] + prev_round[i][1]
    return placar

def find_index(header,string):
    for i in range(0,len(header)):
        if header[i] == string :
            return i
    return -1

def get_game_rounds(open_csv,players):
    
    number_of_games_per_round = len(players)/2
    player_index = make_map_player_index(players)
    rounds = []
    round_ = make_round(None,players)
    count = 0
    for line in open_csv:
        row = line[0].split(';')
        if row[0] == "Div":
            home_player_index = find_index(row,"HomeTeam")
            away_player_index = home_player_index+1
            home_score_index = home_player_index+2
            away_score_index = home_player_index+3
            result_index = home_player_index+4
        if row[0] == "E0":
            if row[result_index] == 'H':
                player = row[home_player_index]
                score = 3
                round_[player_index[player]][1] = round_[player_index[player]][1] + int(score)
            elif row[result_index] == 'A':
                player = row[away_player_index]
                score = 3
                round_[player_index[player]][1] = round_[player_index[player]][1] + int(score)
            elif row[result_index] == 'D':
                player = row[home_player_index]
                score = 1
                round_[player_index[player]][1] = round_[player_index[player]][1] + int(score)
                player = row[away_player_index]
                score = 1
                round_[player_index[player]][1] = round_[player_index[player]][1] + int(score)
            count = count + 1
            if count == number_of_games_per_round :
                count = 0
                rounds.append(round_)
                round_ = make_round(round_,players)
    return rounds
    

def write_premierleague_on_brasileiro_format(gameFilePath,year):
    def player_score(score):
        return score[1]

    with open(abspath(gameFilePath),'r') as filestream:
        open_csv = csv.reader(filestream)
        players = get_players(open_csv)
    #print(year,len(players))
    with open(abspath(gameFilePath),'r') as filestream:
        open_csv = csv.reader(filestream)
        game_rounds = get_game_rounds(open_csv,players)
    #print(year,len(game_rounds))
    for round_ in game_rounds:
        round_.sort(reverse=True,key=player_score)
    with open(abspath('data/ingles/simples'+year),'w') as filestream:
        filestream.write("[")
        number_of_game_rounds = len(game_rounds)
        for count in range(0,number_of_game_rounds):
            game_round = game_rounds[count]
            filestream.write("[")
            sz = len(game_round)
            for index in range(0,sz):
                score = game_round[index]
                filestream.write("[")
                filestream.write('"')
                filestream.write(score[0])
                filestream.write('"')
                filestream.write(",")
                filestream.write(str(score[1]))
                filestream.write("]")
                if(index < sz-1): filestream.write(",")
            filestream.write("]")
            if count < number_of_game_rounds-1 : filestream.write(",")
        filestream.write("]")


if __name__ == "__main__":
    configreader = configReader.ConfigReader()
    folder = abspath(configreader.parser.get('folder ingles','folder'))
    for fil in os.listdir(folder):
        if fil.startswith("premier-league-") :
            path = folder + os.sep + fil
            write_premierleague_on_brasileiro_format(path,path[-8:-4])
    pass