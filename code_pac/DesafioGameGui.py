from __future__ import division
import wx
import wx.grid
from wx import Frame
import dataBaseAdapter
from GameQualityAssessment.code_pac.desafio.model import  Tournament, Series, Game
from GameQualityAssessment.code_pac.model import DesafioGame
import matplotlib
from wx.lib.agw.pyprogress import PyProgress


matplotlib.use('WxAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import numpy as np

import multiprocessing as mp
import time

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class GUIDesafioGame(Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GUIDesafioGameView.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, "Tournament")
        self.lstTournament = wx.ListBox(self, wx.ID_ANY)
        self.label_2 = wx.StaticText(self, wx.ID_ANY, "Series")
        self.lstSeries = wx.ListBox(self, wx.ID_ANY, style=wx.LB_SINGLE)
        self.label_3 = wx.StaticText(self, wx.ID_ANY, "Game")
        self.lstGame = wx.ListBox(self, wx.ID_ANY, style=wx.LB_SINGLE)
        self.gridPointsRows = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
        self.label_4 = wx.StaticText(self, wx.ID_ANY, "Assessment")
        self.lstAssessment = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.lstAssessment.InsertColumn(0, 'Code', width=50)
        self.lstAssessment.InsertColumn(1, 'Measure', width=150)
        self.lstAssessment.InsertColumn(2, 'Ver.', width=50)
        self.lstAssessment.InsertColumn(3, 'Value', width=125)
        self.label_5 = wx.StaticText(self, wx.ID_ANY, "Overall evaluation")
        self.txtOverall = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_6 = wx.StaticText(self, wx.ID_ANY, "History by Points")
        #self.window_1 = CustomWidget(self, wx.ID_ANY)
        
        self.pointsGraph = panel_plot(self)
        self.positionGraph = panel_plot(self)
        
        self.label_7 = wx.StaticText(self, wx.ID_ANY, "History by Position")
        #self.window_2 = CustomWidget(self, wx.ID_ANY)
        
        
        self.Bind(wx.EVT_LISTBOX, self._onLstTournament, self.lstTournament)
        self.Bind(wx.EVT_LISTBOX, self._onLstSeries, self.lstSeries)
        self.Bind(wx.EVT_LISTBOX, self._onLstGame, self.lstGame)
        self.Bind(wx.EVT_SIZE, self._myResize, self)
        
        self.__set_properties()
        self.__do_layout()
        # end wxGlade
        
    def _myResize(self, event):
        self.Layout()
        self.pointsGraph.set_size()
        self.positionGraph.set_size()

    def __set_properties(self):
        # begin wxGlade: GUIDesafioGameView.__set_properties
        self.SetTitle(gettext.gettext("Match Viewer"))
        #self.lstTournament.SetSelection(0)
        self.__fillBlankGrid()
        #self.pointsGraph.SetBackgroundColour(wx.WHITE)
        # end wxGlade
    
    def __fillBlankGrid(self):
        self.gridPointsRows.CreateGrid(37, 9)
        self.gridPointsRows.EnableEditing(0)
        self.gridPointsRows.EnableDragRowSize(0)
        self.gridPointsRows.SetSelectionMode(wx.grid.Grid.wxGridSelectColumns)
        self.gridPointsRows.SetColSize(0, 10)
        self.gridPointsRows.SetColSize(1, 10)
        self.gridPointsRows.SetColSize(2, 10)
        self.gridPointsRows.SetColSize(3, 10)
        self.gridPointsRows.SetColSize(4, 10)
        self.gridPointsRows.SetColSize(5, 10)
        self.gridPointsRows.SetColSize(6, 10)
        self.gridPointsRows.SetColSize(7, 10)
    
    def __clearGrid(self):
        while not self.gridPointsRows.GetNumberRows() == 0:
            self.gridPointsRows.DeleteRows()
        while not self.gridPointsRows.GetNumberCols() == 0:
            self.gridPointsRows.DeleteCols()
            
    def __do_layout(self):
        # begin wxGlade: GUIDesafioGameView.__do_layout
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_16 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_7.Add((20, 10), 0, 0, 0)
        sizer_8.Add((10, 20), 0, 0, 0)
        sizer_11.Add(self.label_1, 0, 0, 0)
        sizer_11.Add(self.lstTournament, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_11, 1, wx.EXPAND, 0)
        sizer_10.Add((20, 20), 0, 0, 0)
        sizer_12.Add(self.label_2, 0, 0, 0)
        sizer_12.Add(self.lstSeries, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_10.Add((20, 20), 0, 0, 0)
        sizer_13.Add(self.label_3, 0, 0, 0)
        sizer_13.Add(self.lstGame, 1, wx.EXPAND, 0)
        sizer_10.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_14.Add((20, 20), 0, 0, 0)
        sizer_14.Add(self.gridPointsRows, 1, wx.EXPAND, 0)
        sizer_9.Add(sizer_14, 1, wx.EXPAND, 0)
        sizer_8.Add(sizer_9, 3, wx.EXPAND, 0)
        sizer_8.Add((20, 20), 0, 0, 0)
        sizer_15.Add(self.label_4, 0, 0, 0)
        sizer_15.Add(self.lstAssessment, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        sizer_15.Add((20, 20), 0, 0, 0)
        sizer_15.Add(self.label_5, 0, 0, 0)
        sizer_15.Add(self.txtOverall, 0, wx.EXPAND, 0)
        sizer_8.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_8.Add((10, 20), 0, 0, 0)
        sizer_7.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_7.Add((20, 20), 0, 0, 0)
        sizer_16.Add((10, 20), 0, 0, 0)
        sizer_17.Add(self.label_6, 0, 0, 0)
        sizer_17.Add(self.pointsGraph, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_16.Add((20, 20), 0, 0, 0)
        sizer_18.Add(self.label_7, 0, 0, 0)
        sizer_18.Add(self.positionGraph, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_18, 1, wx.EXPAND, 0)
        sizer_16.Add((10, 20), 0, 0, 0)
        sizer_7.Add(sizer_16, 1, wx.EXPAND, 0)
        sizer_7.Add((20, 10), 0, 0, 0)
        self.SetSizer(sizer_7)
        sizer_7.Fit(self)
        self.Layout()
        # end wxGlade
    
    def fillTournament(self):
        conn = dataBaseAdapter.getConnection()
        tournaments = sorted(Tournament.retriveList(conn), key=lambda  tournament: tournament.tournamentCode)
        dataBaseAdapter.closeConnection(conn)
        self.lstSeries.Clear()
        self.lstGame.Clear()
        for tournament in tournaments:
            i = len(self.lstTournament.GetItems())
            self.lstTournament.Insert(tournament.country.strip() + " - " + str(tournament.refYear), i, tournament)
    
    def _fillSeries(self, inputTournament):
        conn = dataBaseAdapter.getConnection()
        seriesList = sorted(Series.retrieveList(inputTournament, conn), key=lambda series: series.seriesOrder)
        dataBaseAdapter.closeConnection(conn)
        self.lstSeries.Clear()
        self.lstGame.Clear()
        self.lstAssessment.DeleteAllItems()
        self.__clearGrid()
        self.pointsGraph.figure.clf()
        self.positionGraph.figure.clf()
        for series in seriesList:
            i = len(self.lstSeries.GetItems())
            self.lstSeries.Insert(str(series.seriesOrder) + " - " + str(series.seriesCode), i, series)
        
            
    def _fillGames(self, inputSeries):
        dlg = wx.ProgressDialog("wait", "Loading games...", 100, self)
        manager = mp.Manager()
        rVal = manager.list()
        self.__getGames(inputSeries, rVal)
		#p = mp.Process(target=self.__getGames, args=(inputSeries, rVal,))
        #p.start()
        #p.join()
        
        games = rVal
        
        self.lstGame.Clear()
        self.lstAssessment.DeleteAllItems()
        self.pointsGraph.figure.clf()
        self.positionGraph.figure.clf()
        self.__clearGrid()
        for game in games:
            dlg.Pulse()
            i = len(self.lstGame.GetItems())
            self.lstGame.Insert(str(i) + " - " + str(game.groupCode), i, game)
        dlg.Destroy()
        
    def __getGames(self, inputSeries, rVal):
        conn = dataBaseAdapter.getConnection()
        rVal += sorted(Game.retrieveList(inputSeries, conn), key=lambda game: game.groupCode)
        dataBaseAdapter.closeConnection(conn)
         
        
    def _fillMeasures(self, inputGame):
        conn = dataBaseAdapter.getConnection()
        measures = inputGame.retrieveMeasureList(conn, "last")
        dataBaseAdapter.closeConnection(conn)
        self.lstAssessment.DeleteAllItems()
        self.txtOverall.SetValue('')
        overallValue = 0
        index = 0
        for measure in measures:
            self.lstAssessment.InsertItem(index, str(measure['measurecode']))
            self.lstAssessment.SetItem(index, 1, measure['measuredescription'])
            self.lstAssessment.SetItem(index, 2, str(measure['measureversion']))
            self.lstAssessment.SetItem(index, 3, str(measure['measurevalue']))
            #byPath-2 uncertainty-3 leadChang-4
            if measure['measurecode'] == 2 or \
                measure['measurecode'] == 3 or \
                measure['measurecode'] == 4:  
                overallValue += measure['measurevalue']
            index += 1
        self.txtOverall.SetValue(str(overallValue / 3))
    
    def _fillTable(self, inputGame):
        obj = DesafioGame(inputGame)
        self.__clearGrid()
        self.gridPointsRows.InsertRows(pos=0, numRows=obj.getNumberRounds())
        self.gridPointsRows.InsertCols(pos=0, numCols=len(obj.getPlayers()))
        col = 0
        for player in obj.getPlayers():
            row = 0
            for r in obj.getGameStruct():
                for individualResult in r[1]:
                    if individualResult.playerCode == player:
                        self.gridPointsRows.SetCellValue(row, col, str(individualResult.totalScore))
                        row += 1 #go to next round to find same player result
            col += 1 #next player, next col
            
    def _onLstTournament(self, event):
        self._fillSeries(event.GetClientData())
        
    def _onLstSeries(self, event):
        if event.IsSelection():
            self._fillGames(event.GetClientData())
    
    def _onLstGame(self, event):
        if event.IsSelection():
            selectecGame = event.GetClientData()
            self._fillMeasures(selectecGame)
            self._fillTable(selectecGame)
            self._plotPoints(selectecGame)
            self._plotPositions(selectecGame)
            
    def _plotPoints(self, inputGame):
        obj = DesafioGame(inputGame)
        players = obj.getPlayers()
        gameObj = obj.getGameStruct()
        self.pointsGraph.figure.clf()
        axes = self.pointsGraph.figure.gca()
        
        #x = xrange(1, len(gameObj)+1)
        x = xrange(2, len(gameObj)+1) #ignoring the first round
        for player in players:
            y=[]
            for i in range(1, len(gameObj)):
                found = False
                for result in gameObj[i][1]:
                    if result.playerCode == player:
                        found = True
                        y.append(result.totalScore)
                if not found:
                    y.append(float(0))
            axes.plot(x,y,'o-',linewidth=2)
        
        axes.set_ylabel('Points')
        axes.set_xlabel('Turn')
        axes.hlines(axes.get_yticks(),2, len(gameObj), colors='0.75')
        axes.vlines(axes.get_xticks(), axes.get_ylim()[0], axes.get_ylim()[1], colors='0.75')
        self.pointsGraph.draw()   
    
    def _plotPositions(self, inputGame):
        obj = DesafioGame(inputGame)
        players = obj.getPlayers()
        gameObj = obj.getGameStruct()
        self.positionGraph.figure.clf()
        axes = self.positionGraph.figure.gca()    
        
        #x = xrange(1, len(gameObj)+1)
        x = xrange(2, len(gameObj)+1) #ignoring the first round
        for player in players:
            y=[]
            #for i in range(0, len(gameObj)):
            for i in range(1, len(gameObj)):
                if i == 0: #every one starts in same position
                    #y.append(len(jogadores))
                    y.append(1)
                else:
                    found = False
                    for result in gameObj[i][1]:
                        if result.playerCode == player:
                            found = True
                            y.append(gameObj[i][1].index(result) + 1)
                    if not found:
                        y.append(len(players))
            y = np.array(y)
            axes.plot(x,y,'o-',linewidth=2)
        #plt.ylim(0, len(self._players)+1)
        axes.set_yticks(xrange(0,len(players)+1))
        axes.set_ylabel('Position')
        axes.set_xlabel('Turn')
        axes.hlines(axes.get_yticks(),2, len(gameObj), colors='0.75')
        axes.vlines(axes.get_xticks(), axes.get_ylim()[0], axes.get_ylim()[1], colors='0.75')
        axes.invert_yaxis()    
        self.positionGraph.draw()
    
    
                
# end of class GUIDesafioGameView



class panel_plot(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        ''', style = wx.NO_FULL_REPAINT_ON_RESIZE'''

        self.figure = Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)

        self.set_size()
        self.draw()

        self._resize_flag = False

    def on_idle(self, event):
        if self._resize_flag:
            self._resize_flag = False
            self.set_size()

    '''def on_size(self, event):
        self._resize_flag = True
    '''
    def set_size(self):
        pixels = tuple(self.GetSize())
        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches([float(x) / self.figure.get_dpi() for x in pixels])

    def draw(self):
        self.canvas.draw()



if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.App(0)
    wx.InitAllImageHandlers()
    desafioGUI = GUIDesafioGame(None, wx.ID_ANY, "")
    desafioGUI.fillTournament()
    desafioGUI.Update()
    app.SetTopWindow(desafioGUI)
    desafioGUI.Show()
    app.MainLoop()
