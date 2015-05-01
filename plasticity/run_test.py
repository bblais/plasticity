#!/usr/bin/env python

__version__= "$Version: $"
__rcsid__="$Id: $"

#import wx
import matplotlib
matplotlib.use('WX')

from numpy import linspace
from utils import *
from dialogs.waxy import *
from dialogs import *
from run_sim import *

import pylab
gray=pylab.cm.gray

from matplotlib.backends.backend_wxagg import FigureCanvasWx as FigureCanvas
from matplotlib.backends.backend_wx import FigureManager
from matplotlib.figure import Figure
from matplotlib.axes import Subplot


class MainFrame(Frame):

    def __init__(self,parent=None,title='',direction='H',
                    size=(750,750),lfname=None):

        Frame.__init__(self,parent,title,direction,size)
    
    def Body(self):
        
        self.CreateMenu()
        self.CenterOnScreen()
        
        self.fig = Figure(figsize=(7,5),dpi=100)
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.figmgr = FigureManager(self.canvas, 1, self)

#        self.axes = [self.fig.add_subplot(221),
#                    self.fig.add_subplot(222),
#                    self.fig.add_subplot(223),
#                    self.fig.add_subplot(224)]
                    
        self.axis=self.fig.add_subplot(1,2,1)
        self.AddComponent(self.canvas)
        self.Plot()

    def Plot(self):
        
        self.axis.hold(False)
        for i in range(1):
            x=linspace(0,200.0,201)
            self.axis.plot(x,x**2*sin(x/200),'-o')
            self.axis.hold(True)
        
            
        self.canvas.draw()
        self.canvas.gui_repaint()
            
            
    
        

    def CreateMenu(self):
    
        menubar = MenuBar()

        menu = Menu(self)
        menu.Append("&Quit", self.Quit, "Quit",hotkey="Ctrl+Q")

        menubar.Append(menu, "&File")

        self.SetMenuBar(menubar)
        self.CreateStatusBar()

        
    def Quit(self,event=None):
        
        
        self.Close()
        

if __name__ == '__main__':

    app = Application(MainFrame, title="Plasticity",lfname=None)
    app.Run()
    
