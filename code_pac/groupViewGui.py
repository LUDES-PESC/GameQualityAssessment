#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sun Jun 14 20:17:38 2015
#
from __future__ import division
import wx
import time
import dataBaseAdapter as db
from GameQualityAssessment.code_pac.desafio.model import Tournament, Series, Game
from GameQualityAssessment.code_pac.model import DesafioGame
from wx.lib.agw.pyprogress import PyProgress
from GameQualityAssessment.code_pac import dataBaseAdapter
from GameQualityAssessment.code_pac.plots.panelPlot import PanelPlot
from GameQualityAssessment.code_pac.plots import singlePlots as SP
from GameQualityAssessment.code_pac.measures import DramaByPointsUp2First, DramaByPositionUp2First, MeasureType

# begin wxGlade: dependencies
import gettext
#from wxPyhton._core import wxBoxSizer

# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class GroupView(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: GroupView.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.tabPanel = wx.Panel(self)
        self.label_5 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Game Exploring")
        self.treeGameExploring = wx.TreeCtrl(self.tabPanel, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER)
        self.label_6 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Tournament:")
        self.valTournament = wx.StaticText(self.tabPanel, wx.ID_ANY, "valTournament")
        self.label_7 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Series:")
        self.valSeries = wx.StaticText(self.tabPanel, wx.ID_ANY, "valSeries")
        self.label_8 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Game:")
        self.valGame = wx.StaticText(self.tabPanel, wx.ID_ANY, "valGame")
        self.label_11 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Games qty. :")
        self.valQTYGame = wx.StaticText(self.tabPanel, wx.ID_ANY, "00000")
        self.lstMeasures = wx.ListCtrl(self.tabPanel, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.label_10 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Overall evaluation")
        self.txtOverallEvaluation = wx.TextCtrl(self.tabPanel, wx.ID_ANY, "")
        self.label_9 = wx.StaticText(self.tabPanel, wx.ID_ANY, "Graph type")
        self.cmbGraphType = wx.ComboBox(self.tabPanel, wx.ID_ANY, choices=['Drama by Points', 'Drama by Position', 'Overall Evaluation'], style=wx.CB_DROPDOWN | wx.CB_SIMPLE)
        self.panelGraph = PanelPlot(self.tabPanel)#wx.Panel(self, wx.ID_ANY)

        self.__set_properties()
        self._fillExploring()
        self._allSetValues()
        self.__do_layout()

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.exploringSelectionChanged, self.treeGameExploring)
        self.Bind(wx.EVT_COMBOBOX, self.cmbGraphChanged, self.cmbGraphType)
        self.Bind(wx.EVT_SIZE, self._myResize, self)
        self.valuesContainer
        
        # end wxGlade

    def _myResize(self, event):
        self.Layout()
        self.panelGraph.set_size()
                
    def _fillExploring(self):
        root = self.treeGameExploring.AddRoot('Tournaments')
        conn = db.getConnection()
        tournaments = Tournament.retriveList(conn)
        #tList = []
        for t in tournaments:
            tVal = t.country.strip() + " - " + str(t.refYear) + " - " + "(code: " + str(t.tournamentCode) + ")"
            node = self.treeGameExploring.AppendItem(parent=root, text=tVal, data=t)
            series = sorted(Series.retrieveList(t, conn), key=lambda series: series.seriesOrder)
            #sList=[]
            for s in series:
                sVal = str(s.seriesOrder) + " - " + str(s.seriesCode)
                node2 = self.treeGameExploring.AppendItem(node, sVal, data=s)
                games = Game.retrieveList(s, conn)
                i = 0
                for g in games:
                    gVal = str(i) + " - " + str(g.groupCode)
                    self.treeGameExploring.AppendItem(node2, gVal, data=g)
                    i += 1
             
            
        db.closeConnection(conn)
            

    def __set_properties(self):
        # begin wxGlade: GroupView.__set_properties
        self.SetTitle("Group Viewer")
        self.SetSize(750, 600)
        self.lstMeasures.InsertColumn(0, 'Code', width=50)
        self.lstMeasures.InsertColumn(1, 'Measure', width=150)
        self.lstMeasures.InsertColumn(2, 'Ver.', width=50)
        self.lstMeasures.InsertColumn(3, 'Value', width=125)
        order = (self.treeGameExploring, self.lstMeasures, self.txtOverallEvaluation, self.cmbGraphType)
        for i in range(len(order) - 1):
            order[i+1].MoveAfterInTabOrder(order[i])
        self._fillComboGraphType()
        #wx.IdleEvent.SetMode(wx.IDLE_PROCESS_SPECIFIED)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: GroupView.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(self.label_5, 0, 0, 0)
        sizer_7.Add(self.treeGameExploring, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_6.Add((10, 20), 0, 0, 0)
        sizer_10.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_10.Add(self.valTournament, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_8.Add(sizer_10, 0, wx.LEFT | wx.TOP | wx.EXPAND, 6)
        sizer_11.Add(self.label_7, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_11.Add(self.valSeries, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_8.Add(sizer_11, 0, wx.LEFT | wx.TOP | wx.EXPAND, 6)
        sizer_12.Add(self.label_8, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_12.Add(self.valGame, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_8.Add(sizer_12, 0, wx.LEFT | wx.TOP | wx.BOTTOM | wx.EXPAND, 6)
        sizer_14.Add(self.label_11, 0, 0, 0)
        sizer_14.Add(self.valQTYGame, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_8.Add(sizer_14, 0, wx.LEFT | wx.EXPAND, 6)
        sizer_8.Add(self.lstMeasures, 1, wx.TOP | wx.EXPAND, 5)
        sizer_13.Add(self.label_10, 0, 0, 0)
        sizer_13.Add(self.txtOverallEvaluation, 0, wx.EXPAND, 0)
        sizer_8.Add(sizer_13, 0, wx.EXPAND, 0)
        sizer_6.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_6, 1, wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, 6)
        sizer_9.Add(self.label_9, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_9.Add(self.cmbGraphType, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_9, 0, wx.LEFT | wx.RIGHT | wx.TOP, 6)
        sizer_5.Add(self.panelGraph, 1, wx.EXPAND, 0)
        sizer_tab.Add(self.tabPanel, 1, wx.EXPAND, 0)
        self.tabPanel.SetSizer(sizer_5)
        self.SetSizer(sizer_tab)
        #self.SetSizer(sizer_5)
        self.tabPanel.Layout()
        self.Layout()
        #self.tabPanel.Layout()
        self.panelGraph.set_size()
        
        # end wxGlade
        
    def _allSetValues(self):
        self.valTournament.SetLabel("ALL")
        self.valSeries.SetLabel("ALL")
        self.valGame.SetLabel("ALL")
        tournaments = self._getChildrenList(self.treeGameExploring.GetRootItem())
        series=[]
        games=[]
        for t in tournaments:
            series += self._getChildrenList(t)
        for s in series:
            games += self._getChildrenList(s)
            
        self.valQTYGame.SetLabel(str(len(games)))
        self._fillLstMeasures(games)
        self._fillGraphPanel(self.valuesContainer)
        #self._fillComboGraphType()    

    def _tournamentSetValues(self, tournament, acItem):
        self.valTournament.SetLabel(self.treeGameExploring.GetItemText(acItem))
        self.valSeries.SetLabel("ALL")
        self.valGame.SetLabel("ALL")
        
        #listing games
        series = self._getChildrenList(acItem)
        games = []
        for s in series:
            games += self._getChildrenList(s)
            
        self.valQTYGame.SetLabel(str(len(games)))
        self._fillLstMeasures(games)
        self._fillGraphPanel(self.valuesContainer)
        #self._fillComboGraphType()
        
    def _seriesSetValues(self, series, acItem):
        tournamentItem = self.treeGameExploring.GetItemParent(acItem)
        self.valTournament.SetLabel(self.treeGameExploring.GetItemText(tournamentItem))
        self.valSeries.SetLabel(self.treeGameExploring.GetItemText(acItem))
        self.valGame.SetLabel("ALL")
        games = self._getChildrenList(acItem)
        self.valQTYGame.SetLabel(str(len(games)))
        self._fillLstMeasures(games)
        self._fillGraphPanel(self.valuesContainer)
        #self._fillComboGraphType()
        
        
    def _fillComboGraphType(self):
        self.cmbGraphType.SetItems(['Choose a graph type ...','Drama by Points', 'Drama by Position', 'Drama by Paths', 'Lead Change', 'Uncertainty'])
        self.cmbGraphType.SetSelection(0)
        
    def _gameSetValues(self, game, acItem):
        seriesItem = self.treeGameExploring.GetItemParent(acItem)
        tournamentItem = self.treeGameExploring.GetItemParent(seriesItem)
        self.valTournament.SetLabel(self.treeGameExploring.GetItemText(tournamentItem))
        self.valSeries.SetLabel(self.treeGameExploring.GetItemText(seriesItem))
        self.valGame.SetLabel(self.treeGameExploring.GetItemText(acItem))
        self.valQTYGame.SetLabel("1")
        #fill measures single game
        self.lstMeasures.DeleteAllItems()
        self.txtOverallEvaluation.SetValue('')
        conn = dataBaseAdapter.getConnection()
        measures = self.treeGameExploring.GetItemData(acItem).retrieveMeasureList(conn)
        #fillLst
        overallValue = 0
        index = 0
        for m in measures:
            self.lstMeasures.InsertItem(index, str(m['measurecode']))
            self.lstMeasures.SetItem(index, 1, m['measuredescription'])
            self.lstMeasures.SetItem(index, 2, str(m['measureversion']))
            self.lstMeasures.SetItem(index, 3, str(m['measurevalue']))
            #byPath-2 uncertainty-3 leadChang-4
            if m['measurecode'] == 2 or \
                m['measurecode'] == 3 or \
                m['measurecode'] == 5:  
                overallValue += m['measurevalue']
            index += 1
        #self._fillComboGraphType()
        #overall drama_by_path + uncertainty + lead_change over 3
        self.txtOverallEvaluation.SetValue(str(overallValue / 3))
        
        self._fillGraphPanel()
        dataBaseAdapter.closeConnection(conn)
        
        
        
    def _getChildrenList(self, inputItem):
        childrenList = []
        child, cookie = self.treeGameExploring.GetFirstChild(inputItem)
        while child.IsOk():
            childrenList.append(child)
            child, cookie = self.treeGameExploring.GetNextChild(inputItem, cookie)
        return childrenList
    
    
    def _fillLstMeasures(self, games):
        self.lstMeasures.DeleteAllItems()
        self.txtOverallEvaluation.SetValue('')
        if not type(games) == list:
            raise TypeError('First arg has to be a list of games')
        
        #get measures
        #fistMeasure
        connection = dataBaseAdapter.getConnection()
        if type(games) == list:
            measuresControl = self.treeGameExploring.GetItemData(games[0]).retrieveMeasureList(connection)
        nMeasures = len(measuresControl)
        
        # initializing measuresSum
        measuresValues = {}
        for m in measuresControl:
            #measuresValues.append(m['measurecode'])
            measuresValues[m['measurecode']] = []
        
        #sum values
        dlg = wx.ProgressDialog("Wait", "Loading Values...", len(games), self)
        pulseCount = 1
        for g in games:
            if pulseCount % 15 == 0:
                #dlg.UpdatePulse()
                dlg.Update(pulseCount)
            pulseCount += 1
            
            gMeasures = self.treeGameExploring.GetItemData(g).retrieveMeasureList(connection)
            if not len(gMeasures) == nMeasures:
                raise Exception('There is an error in measures stored.')
            for m in gMeasures:
                measuresValues[m['measurecode']].append(m['measurevalue'])
         
        #average
        measuresAvg={}
        for m in measuresControl:
            #measuresAvg.append(m['measurecode'])
            measuresAvg[m['measurecode']] = sum(measuresValues[m['measurecode']]) / len(games)    
                
        #fillLst
        index = 0
        for m in measuresControl:
            self.lstMeasures.InsertItem(index, str(m['measurecode']))
            self.lstMeasures.SetItem(index, 1, m['measuredescription'])
            self.lstMeasures.SetItem(index, 2, str(m['measureversion']))
            self.lstMeasures.SetItem(index, 3, str(measuresAvg[m['measurecode']]))
            index += 1
        
        #overall drama_by_path + uncertainty + lead_change over 3
        overallEvaluation = (measuresAvg[2] + measuresAvg[5] + measuresAvg[3]) / 3
        
        self.txtOverallEvaluation.SetValue(str(overallEvaluation))
        
        dataBaseAdapter.closeConnection(connection)
        dlg.Destroy()
        self.treeGameExploring.SetFocus()
        self.valuesContainer =  measuresValues
    
    def _fillGraphPanel(self, values=None):
        selected = self.treeGameExploring.GetSelection()
        cmbValue = self.cmbGraphType.GetValue() 
        if cmbValue == 'Choose a graph type ...':
            self.panelGraph.figure.clear()
            self.panelGraph.draw()
            return
        
        if selected.IsOk:
            selectedData = self.treeGameExploring.GetItemData(selected)
            if isinstance(selectedData, Game):
                if cmbValue == 'Drama by Position':
                    SP.position(selectedData, self.panelGraph, ignored=1)
        
                if cmbValue == 'Drama by Points':
                    SP.points(selectedData, self.panelGraph, ignored=1)
                    
                if cmbValue == 'Drama by Paths':
                    SP.position(selectedData, self.panelGraph, ignored=1)
                
                if cmbValue == 'Lead Change':
                    SP.position(selectedData, self.panelGraph, ignored=1)
                    
                if cmbValue == 'Uncertainty':
                    SP.points(selectedData, self.panelGraph, ignored=1)
                    
            else:
                if cmbValue == 'Drama by Position':
                    SP.histGeral(values[1], self.panelGraph, cmbValue)
                if cmbValue == 'Drama by Points':
                    SP.histGeral(values[0], self.panelGraph, cmbValue)
                if cmbValue == 'Drama by Paths':
                    SP.histGeral(values[2], self.panelGraph, cmbValue)
                if cmbValue == 'Uncertainty':
                    SP.histGeral(values[5], self.panelGraph, cmbValue)   
                if cmbValue == 'Lead Change':
                    SP.histGeral(values[3], self.panelGraph, cmbValue)
                
                    
    def exploringSelectionChanged(self, event):  # wxGlade: GroupView.<event_handler>
        acItem = event.GetItem()
        acData = self.treeGameExploring.GetItemData(acItem)
        
        if acItem == self.treeGameExploring.GetRootItem():
            self._allSetValues()
        
        if isinstance(acData, Tournament):
            self._tournamentSetValues(acData, acItem)
        
        if isinstance(acData, Series):
            self._seriesSetValues(acData, acItem)
        
        if isinstance(acData, Game):
            self._gameSetValues(acData, acItem)
        event.Skip()  
    
    def cmbGraphChanged(self, event):  # wxGlade: GroupView.<event_handler>
        self._fillGraphPanel(self.valuesContainer)            
                
            
        event.Skip()       
        
        

# end of class GroupView
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name
    app = wx.App(0)
    wx.InitAllImageHandlers()
    frame_1 = GroupView(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
