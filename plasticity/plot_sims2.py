#!/usr/bin/env python

from dialogs.waxy import *
#from waxy import *

import os,sys
import glob
from utils import *
import zpickle


import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWx as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Subplot
import pylab
gray=pylab.cm.gray

class PlotFrame(Frame):

    def __init__(self,parent=None,title='',direction='H',
                    size=(800,800)):
        self.fig=None

        Frame.__init__(self,parent,title,direction,size)


    def Body(self):
        
        self.CenterOnScreen()
        self.params=default_params()
        self.ResetTitle()
        
        self.fig = Figure(figsize=(7,5),dpi=100)
        self.axes = [self.fig.add_subplot(221),
                    self.fig.add_subplot(222),
                    self.fig.add_subplot(223),
                    self.fig.add_subplot(224)]
                    
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.CreateStatusBar()
        
        self.Show()

    def ResetTitle(self):
        
        (root,sfname)=os.path.split(self.params['save_sim_file'])
        s=''
            
        title='Plasticity: %s%s' % (sfname,s)
        self.SetTitle(title)

        
    def Plot(self,sim):
        
        sim['params']['display']=True

        if 'display_module' in sim['params']:
            if sim['params']['display_module']:
                try:
                    module=__import__(sim['params']['display_module'],fromlist=['UserPlot'])
                except ImportError:
                    sim['params']['display']=False
                    dlg = MessageDialog(self, 
                            "Error","Error in Import: %s.  Turning display off" % sim['params']['display_module'],
                            icon='error')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
                
                try:
                    module.UserPlot(self,sim)
                    return
                except ValueError:
                    sim['params']['display']=False
                    dlg = MessageDialog(self, 
                            "Error","Error in display.  Turning display off",
                            icon='error')
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
        
        try:
        
            im=weights2image(sim['params'],sim['weights'])
            
            self.axes[0].hold(False)
            self.axes[0].set_axis_bgcolor('k')
            self.axes[0].pcolor(im,cmap=gray,edgecolors='k')
            self.axes[0].set_aspect('equal')
            
            num_moments=sim['moments_mat'].shape[0]
    
            self.axes[1].hold(False)
            for i in range(num_moments):
                self.axes[1].plot(sim['moments_mat'][i,0,:],'-o')
                self.axes[1].hold(True)
            
    
            self.axes[2].hold(False)
            response_mat=sim['response_mat']
            response_var_list=sim['response_var_list']
            styles=['b-o','g-o']
            for i,r in enumerate(response_var_list[-1]):
                x=r[1]
                y=r[2]
            
                self.axes[2].plot(x,y,styles[i])
                self.axes[2].hold(True)
            
                
            self.axes[3].hold(False)
            styles=['b-o','g-o']
            for i,r in enumerate(response_mat):
                self.axes[3].plot(r,styles[i])
                self.axes[3].hold(True)
            
            
                
            self.canvas.draw()
            
        except ValueError:
            sim['params']['display']=False
            dlg = MessageDialog(self, 
                    "Error","Error in display.  Turning display off",
                    icon='error')
            dlg.ShowModal()
            dlg.Destroy()
            
            

    
class MainFrame(Frame):

    def __init__(self,parent=None,title='',direction='v',
                    size=(200,800),default_wildcard=None,default_file_list=[]):

        self.default_wildcard=default_wildcard
        Frame.__init__(self,parent,title,direction,size)
        
    def Body(self):
        
        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")

        if not self.default_wildcard:
            self.default_wildcard='sims/'
            
        wildcard=self.default_wildcard
        
        self.textbox = TextBox(self,Value=wildcard)
        self.textbox.OnText=self.OnChar
        if '*' not in wildcard:
            wildcard+='*'
        
        if not default_file_list:
            files=glob.glob(wildcard)
        else:
            files=default_file_list
        
        self.AddComponent(self.textbox, border=3, expand='h')
        
        
        
        self.listbox = ListBox(self, choices=files, 
                            size=(250, 450), 
                            selection='single')
        
        self.AddComponent(self.listbox, border=3, expand='both')
        self.listbox.OnClick = self.Click
        
        self.Pack()
        
        pos=self.GetPosition()
        pos[0]=0
        self.SetPosition(pos)


        self.plot_frame=PlotFrame(self)
        
    def OnChar(self,event):
        
        event.Skip()
        self.UpdateWildcard()
    
    
    def WatchForEnter(self,event):
        
        event.Skip()
        if event.GetKeyCode()==13:  # enter
            self.UpdateWildcard()
        
    def UpdateWildcard(self,event=None):
        wildcard=self.textbox.Value
        
        if '*' not in wildcard:
            wildcard+='*'
        
        files=glob.glob(wildcard)
        
        self.listbox.Fill(files)
        
        
    def Click(self,event):
    
        
        file=event.GetString()
        
        if file:
            
            self.SetCursor('arrowwait')
            self.plot_frame.SetStatusText('Plotting %s...' % file)
            self.UpdateWindowUI()
            self.Refresh()
            sim=zpickle.load(file)
            self.plot_frame.params=sim['params']
            self.plot_frame.Plot(sim)
            self.SetCursor('default')
            self.plot_frame.SetStatusText('Plotting %s...done.' % file)
        
        
    def CloseWindow(self,event):
        self.Close()
        
def run(default_wildcard=None,default_file_list=[]):
    app = Application(MainFrame, title="Plot Sims",default_wildcard=default_wildcard,default_file_list=[])
    app.Run()

    
if __name__ == '__main__':

    if len(sys.argv)==2:
        default_wildcard=sys.argv[1]
    elif len(sys.argv)>2:
        default_file_list=sys.argv[1:]
        default_wildcard=None
    else:
        default_wildcard=None
        default_file_list=[]

    run(default_wildcard,default_file_list)

