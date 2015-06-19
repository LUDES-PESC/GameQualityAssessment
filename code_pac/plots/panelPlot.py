'''
Created on 15/06/2015

@author: mangeli
'''
import wx
import matplotlib
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx #to future implementation
from matplotlib.figure import Figure

class PanelPlot(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.WS_EX_PROCESS_IDLE)
        ''', style = wx.NO_FULL_REPAINT_ON_RESIZE'''

        self.figure = Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)

        self.set_size()
        self.draw()

        self._resize_flag = False

        #self.Bind(wx.EVT_IDLE, self.on_idle)
        #self.Bind(wx.EVT_SIZE, self.on_size)

    def on_idle(self, event):
        #event.RequestMore() 
        if self._resize_flag:
            self._resize_flag = False
            #wx.CallLater(500,self.set_size())

    def on_size(self, event):
        self._resize_flag = True

    def set_size(self):
        pixels = tuple(self.GetSize())
        self.SetSize(pixels)
        self.canvas.SetSize(pixels)
        self.figure.set_size_inches([float(x) / self.figure.get_dpi() for x in pixels])

    def draw(self):
        self.canvas.draw()