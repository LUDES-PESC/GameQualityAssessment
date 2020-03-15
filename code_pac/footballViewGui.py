import wx
import wx.grid as grid
from GameQualityAssessment.code_pac.model import BrasileiroGame
import GameQualityAssessment.code_pac.brasileiro.model as model
from GameQualityAssessment.code_pac.measures import DramaByPaths as Drama, UncertaintyPDD as Uncertainty, LeadChange
from GameQualityAssessment.code_pac.plots.panelPlot import PanelPlot
import GameQualityAssessment.code_pac.plots.brasileiroPlots as bp

class FootballView(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title="Football View",size=(640,480))
        self.SetMinSize((640,480))
        self.__declareVariables()
        self.__makeSizers()
        self.__fillTree()

        self.dataGrid.CreateGrid(4,1)
        self.dataGrid.SetColLabelValue(0,"Value")
        self.dataGrid.SetColSize(0,100)
        self.dataGrid.SetRowLabelSize(100)
        self.dataGrid.SetRowLabelValue(0,"Drama")
        self.dataGrid.SetRowLabelValue(1,"Uncertainty")
        self.dataGrid.SetRowLabelValue(2,"Lead Change")
        self.dataGrid.SetRowLabelValue(3,"Overall Eval.")
        self.Bind(wx.EVT_SIZE,self.__resize)
        self.gameExplorer.Bind(wx.EVT_TREE_SEL_CHANGED, self.__setData)

        self.__setData(None)
    
    def __resize(self,event):
        self.Layout()
        self.graphShow.GetCurrentPage().set_size()
    
    def __declareVariables(self):
        self.mainPanel = wx.Panel(self)
        self.panelGameExplorer = wx.Panel(self.mainPanel)
        self.gameExplorer = wx.TreeCtrl(self.panelGameExplorer)
        self.panelData = wx.Panel(self.mainPanel)
        self.dataGrid = grid.Grid(self.panelData)
        self.panelGraphShow = wx.Panel(self.mainPanel)
        self.graphShow = wx.Notebook(self.panelGraphShow)
        self.gamesList = model.Game.retrieveList()
        pass

    def __makeSizers(self):
        sizersSizer = wx.BoxSizer(wx.HORIZONTAL)
        lateralSizer = wx.BoxSizer(wx.VERTICAL)
        panelGameExplorerSizer = wx.BoxSizer(wx.VERTICAL)
        panelDataSizer = wx.BoxSizer(wx.VERTICAL)
        panelGraphShowSizer = wx.BoxSizer(wx.VERTICAL)
        
        panelGraphShowSizer.AddSpacer(20)
        panelGraphShowSizer.Add(self.graphShow,1,wx.EXPAND)
        panelGraphShowSizer.AddSpacer(20)
        self.panelGraphShow.SetSizer(panelGraphShowSizer)
        self.graphShow.SetMinSize((200,200))

        panelDataSizer.Add(self.dataGrid)
        self.panelData.SetSizer(panelDataSizer)
        self.dataGrid.SetMinSize((200,108))
        self.dataGrid.SetMaxSize((200,108))

        panelGameExplorerSizer.Add(self.gameExplorer,proportion=1)
        self.panelGameExplorer.SetSizer(panelGameExplorerSizer)
        self.gameExplorer.SetMinSize((200,200))

        lateralSizer.AddSpacer(20)
        lateralSizer.Add(self.panelGameExplorer,10,0,5)
        lateralSizer.AddSpacer(20)
        lateralSizer.Add(self.panelData,proportion=0)
        lateralSizer.AddSpacer(20)

        sizersSizer.AddSpacer(20)
        sizersSizer.Add(lateralSizer,proportion=1)
        sizersSizer.AddSpacer(20)
        sizersSizer.Add(self.panelGraphShow,10, wx.EXPAND)
        sizersSizer.AddSpacer(20)

        self.Maximize(True)
        self.mainPanel.SetSizerAndFit(sizersSizer)
        self.Centre()
        self.Layout()
        pass

    def __fillTree(self):
        root = self.gameExplorer.AddRoot("Games")
        for game in self.gamesList :
            self.gameExplorer.AppendItem(root,game.year,data=game)
        pass

    def __setData(self,event):
        selected = self.gameExplorer.GetSelection()

        games = None
        if selected.IsOk() :
            games = self.gameExplorer.GetItemData(selected)
            if games == None:
                games = self.gamesList
            else:
                games = [games]
        else:
            games = self.gamesList
        
        dramas = []
        uncerts = []
        leadChgs = []
        for game in games :
            brgame = BrasileiroGame(game)
            dramas.append(Drama(game=brgame,ignored=0).getMeasureValue())
            uncerts.append(Uncertainty(game=brgame,ignored=0).getMeasureValue())
            leadChgs.append(LeadChange(game=brgame,ignored=0).getMeasureValue())
        
        self.dataGrid.SetCellValue(0,0,str(sum(dramas)/len(dramas)))
        self.dataGrid.SetCellValue(1,0,str(sum(uncerts)/len(uncerts)))
        self.dataGrid.SetCellValue(2,0,str(sum(leadChgs)/len(leadChgs)))
        # avg(avg_drama,avg_uncert,avg_leadChg)
        # avg(sum_drama/num_games,sum_uncert/num_games,sum_leadChg/num_games)
        # avg(sum_drama,sum_uncert,sum_leadChg)/num_games
        # (sum_drama+sum_uncert+sum_leadChg)/3/num_games
        # (sum_drama+sum_uncert+sum_leadChg)/3*num_games
        self.dataGrid.SetCellValue(3,0,str((sum(dramas)+sum(uncerts)+sum(leadChgs))/(3*len(dramas))))

        for i in range(0,self.graphShow.GetPageCount()):
            page = self.graphShow.GetPage(0)
            self.graphShow.RemovePage(0)
            self.graphShow.RemoveChild(page)
            page.Destroy()
        
        if len(dramas) > 1:
            overall_evals = [(dramas[i]+uncerts[i]+leadChgs[i])/3 for i in range(0,len(dramas))]

            panel_drama = PanelPlot(self.graphShow)
            panel_uncert = PanelPlot(self.graphShow)
            panel_leadChg = PanelPlot(self.graphShow)
            panel_evals = PanelPlot(self.graphShow)
            bp.values_histogram(dramas,panel_drama,'Drama')
            bp.values_histogram(uncerts,panel_uncert,'Uncertainty')
            bp.values_histogram(leadChgs,panel_leadChg,'Lead Change')
            bp.values_histogram(overall_evals,panel_evals,'Overall Eval.')
            self.graphShow.AddPage(panel_drama,"Histogram - Drama")
            self.graphShow.AddPage(panel_uncert,"Histogram - Uncertainty")
            self.graphShow.AddPage(panel_leadChg,"Histogram - Lead Change")
            self.graphShow.AddPage(panel_evals,"Histogram - Overall Eval.")

            panel_drama.draw()
            panel_drama.set_size()
            panel_uncert.draw()
            panel_uncert.set_size()
            panel_leadChg.draw()
            panel_leadChg.set_size()
            panel_evals.draw()
            panel_evals.set_size()
        else:
            panel_points = PanelPlot(self.graphShow)
            panel_positions = PanelPlot(self.graphShow)
            bp.points(games[0],panel_points)
            bp.positions(games[0],panel_positions)
            self.graphShow.AddPage(panel_points,"History by Points")
            self.graphShow.AddPage(panel_positions,"History by Positions")

            panel_points.draw()
            panel_points.set_size()
            panel_positions.draw()
            panel_positions.set_size()
        pass

if __name__ == "__main__":
    app = wx.App() 
    frame = FootballView()
    frame.Show()
    app.MainLoop()