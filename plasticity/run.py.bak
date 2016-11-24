#!/usr/bin/env python

__version__= "$Version: $"
__rcsid__="$Id: $"

import matplotlib
#matplotlib.use('WX')

from wx import MilliSleep
from wx import SplashScreen, SPLASH_CENTRE_ON_SCREEN, SPLASH_TIMEOUT
import os
import sys
import warnings
import zpickle

from utils import *
from dialogs.waxy import *
from dialogs import *
from run_sim import *
import threading

import pylab
gray=pylab.cm.gray

from matplotlib.backends.backend_wxagg import FigureCanvasWx as FigureCanvas
from matplotlib.backends.backend_wx import FigureManager
from matplotlib.figure import Figure
from matplotlib.axes import Subplot

class SimThread(threading.Thread):
    def __init__(self,params,parent):
        self.params=params
        self.parent=parent
        
        threading.Thread.__init__(self);

    def run(self):
        
        run_sim(self.params,self.parent)
                        

def subplot(*args):
    import pylab
    
    if len(args)==1:
        return pylab.subplot(args[0])
        
    elif len(args)==3:
        return pylab.subplot(args[0],args[1],args[2])
        
    elif len(args)==4:

        r=args[2]
        c=args[3]
        
        return pylab.subplot(args[0],args[1],c+(r-1)*args[1]);
        
        
    else:
        raise ValueError,"invalid number of arguments"
    

class MainFrame(Frame):

    def __init__(self,parent=None,title='',direction='H',
                    size=(750,750),lfname=None,params=None):
        self.fig=None
        
        
        # turn off security warning on tmpnam.  why is it here?
        warnings.filterwarnings('ignore')    
        fname=os.tempnam()
        warnings.resetwarnings()
        
        
        self.base_dir=os.path.dirname(__file__)
        if not self.base_dir:
            self.base_dir='.'
            
        self.tmpfile=fname+"_plasticity.dat"
        self.modified=False
        self.running=False
        self.stopping=False
        self.quitting=False
        self.plot_first=False
        
        if not params:
            self.params=default_params()
        else:
            self.params=params
        
        for p in self.params['pattern_input']:
            if not os.path.exists(p['filename']):
                p['filename']=self.base_dir+"/"+p['filename']
        
        
        if lfname:
            if not self.__load_sim__(lfname):
                self.plot_first=True


        Frame.__init__(self,parent,title,direction,size)
    
    def Body(self):
        
        self.CreateMenu()
        self.CenterOnScreen()
        
        self.ResetTitle()
        
        fname=self.base_dir+"/images/plasticity_small_icon.ico"
        self.SetIcon(fname)

        
        self.fig = Figure(figsize=(7,5),dpi=100)
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.figmgr = FigureManager(self.canvas, 1, self)

        self.axes = [self.fig.add_subplot(221),
                    self.fig.add_subplot(222),
                    self.fig.add_subplot(223),
                    self.fig.add_subplot(224)]
                    
        
        if self.plot_first:
            sim=zpickle.load(self.tmpfile)
            sim['params']['display']=True
            self.Plot(sim)

    def Stopping(self):
        return self.stopping
    
    def Yield(self):
        wx.Yield()
    
    def ResetTitle(self):
        
        (root,sfname)=os.path.split(self.params['save_sim_file'])
        if self.modified:
            s=' (*)'
        else:
            s=''
            
        title='Plasticity: %s%s' % (sfname,s)
        self.SetTitle(title)

        
    def Plot(self,sim):
        
        if not sim['params']['display']:
            return

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
            num_neurons=sim['moments_mat'].shape[1]
            for k in range(num_neurons):
                for i in range(num_moments):
                    self.axes[1].plot(sim['moments_mat'][i,k,:],'-o')
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
            self.canvas.gui_repaint()
            
        except ValueError:
            sim['params']['display']=False
            dlg = MessageDialog(self, 
                    "Error","Error in display.  Turning display off",
                    icon='error')
            dlg.ShowModal()
            dlg.Destroy()
            
            
    
    def Run_Pause(self,event):

        if not self.running:
#            pylab.close()
            
            self.params['tmpfile']=self.tmpfile
            if os.path.exists(self.tmpfile):
                self.params['continue']=1
            self.modified=True
            self.ResetTitle()
            self.running=True

##            d={}
##            d['params']=self.params
##            zpickle.save(d,'plasticity_tmpparams.dat')
##            cmd='./run_sim.py --paramfile plasticity_tmpparams.dat --from_gui 1'
##            os.system(cmd)
            self.stopping=False
            run_sim(self.params,self)

            self.params['load_sim_file']=self.tmpfile
            self.running=False
            if self.quitting:
                self.Quit()
        
        else:
            self.stopping=True
    
            
    def __load_sim__(self,lfname):
        
        sim=zpickle.load(lfname)

        params=sim['params']
        
        params['save_sim_file']=self.params['save_sim_file']
        params['load_sim_file']=''
        params['continue']=False
        
        try:
            params['initial_weights']=sim['weights']
            params['initial_moments']=sim['moments']
        except KeyError:
            self.params=params
            return 1

        params['load_sim_file']=self.tmpfile
        params['continue']=True
        sim['params']=params
        self.params=params
        
        zpickle.save(sim,self.tmpfile)
        
        return 0

    def Reset_Simulation(self,event=None):
        if not os.path.exists(self.tmpfile):
            return

        
        self.canvas.Show(False)
        if self.modified:
            (root,sfname)=os.path.split(self.params['save_sim_file'])
            dlg=MessageDialog(self, 
                          text="Do you want to save the changes you made to %s?" % sfname,
                          title="Reset", ok=0, yes_no=1,cancel=1)
            result=dlg.ShowModal()
            dlg.Destroy()
            
            if result == 'cancel':
                self.canvas.Show(True)
                return
            elif result == 'yes':
                filename=self.Save_Simulation()
                if not filename: # cancelled the save
                    self.canvas.Show(True)
                    return
        
        
        
        self.params['continue']=False
        self.params['load_sim_file']=''
        self.params['initial_weights']=[]
        self.params['initial_moments']=[]
        

        for a in self.axes:
            
            a.cla()

        self.canvas.draw()    
        self.canvas.Show(True)
        
        
        
        
    def Restart(self,event=None):
        
        if not os.path.exists(self.tmpfile):
            return
        
        self.canvas.Show(False)
        if self.modified:
            (root,sfname)=os.path.split(self.params['save_sim_file'])
            dlg=MessageDialog(self, 
                          text="Do you want to save the changes you made to %s?" % sfname,
                          title="Restart", ok=0, yes_no=1,cancel=1)
            result=dlg.ShowModal()
            dlg.Destroy()
            
            if result == 'cancel':
                self.canvas.Show(True)
                return
            elif result == 'yes':
                filename=self.Save_Simulation()
                if not filename: # cancelled the save
                    self.canvas.Show(True)
                    return
        
        
        
        
        self.__load_sim__(self.tmpfile)
        self.params['continue']=False
        self.canvas.Show(True)
        
        
    def Load_Simulation(self,event=None):

        self.canvas.Show(False)
        if self.modified:
            (root,sfname)=os.path.split(self.params['save_sim_file'])
            dlg=MessageDialog(self, 
                          text="Do you want to save the changes you made to %s?" % sfname,
                          title="Load Simulation", ok=0, yes_no=1,cancel=1)
            result=dlg.ShowModal()
            dlg.Destroy()
            
            if result == 'cancel':
                pass
            elif result == 'yes':
                self.Save_Simulation()
                
        lfname=''    
        dlg = FileDialog(self, "Load Simulation",default_dir=os.getcwd()+"/sims",
                        wildcard='DAT Files|*.dat|All Files|*.*')
        result = dlg.ShowModal()
        if result == 'ok':
            lfname = dlg.GetPaths()[0]
        dlg.Destroy()

        if not lfname:
            self.canvas.Show(True)
            return
        
        self.__load_sim__(lfname)
            
        sim=zpickle.load(self.tmpfile)
        self.Plot(sim)
        self.canvas.Show(True)
            
    def Save_Simulation(self,event=None):
        
        if not self.modified:
            return
        
        sfname=self.params['save_sim_file']
        def_sfname=default_params()['save_sim_file']
        if sfname==def_sfname:
            filename=self.Save_Simulation_As()
            
            
        else:
            filename=sfname
            d=zpickle.load(self.tmpfile)
            d['params']=self.params
            zpickle.save(d,sfname)
            
            self.modified=False
            
            self.ResetTitle()

        return filename
    
    def Save_Simulation_As(self,event=None):
        
        self.canvas.Show(False)
        dlg = FileDialog(self, "Save Simulation As...",default_dir=os.getcwd()+"/sims/",
                        wildcard='DAT Files|*.dat|All Files|*.*',save=1)
        result = dlg.ShowModal()
        if result == 'ok':
            filename = dlg.GetPaths()[0]
        else:
            filename=None
            
        dlg.Destroy()

            
        if filename:
            d=zpickle.load(self.tmpfile)
            self.params['save_sim_file']=filename
            d['params']=self.params
            zpickle.save(d,filename)
            
            self.modified=False
            
            self.ResetTitle()
        
        self.canvas.Show(True)
            
        return filename
    
    def Set_Simulation_Parameters(self,event):
        self.canvas.Show(False)
        set_simulation_parameters(self.params,self)
        self.canvas.Show(True)
        
    def Set_Input_Parameters(self,event):
        self.canvas.Show(False)
        set_input_parameters(self.params,self)
        self.canvas.Show(True)
        
    def Set_Output_Parameters(self,event):
        self.canvas.Show(False)
        set_output_parameters(self.params,self)
        self.canvas.Show(True)
        
    def Set_Weight_Parameters(self,event):
        self.canvas.Show(False)
        set_weight_parameters(self.params,self)
        self.canvas.Show(True)

    def Save_Parameters_As(self,event):
        save_parameters_as(self.params,self)
        
    def Set_Parameter_Structure(self,event):
        set_parameter_structure(self.params,self)

    def Load_Parameters(self,event):
        p=load_parameters(None,self)
        if p:
            self.params=p
        
    def CreateMenu(self):
    
        menubar = MenuBar()

        menu = Menu(self)
        menu.Append("L&oad State", self.Load_Simulation, "Load a Complete Simulation",hotkey="Ctrl+O")
        menu.Append("Load &Parameters", self.Load_Parameters, "Load Simulation Parameters")
        menu.AppendSeparator()
        menu.Append("Save Parameters As...", self.Save_Parameters_As, "Save Simulation Parameters")
        menu.Append("Save State As...", self.Save_Simulation_As, "Save a Complete Simulation")
        menu.Append("Save State", self.Save_Simulation, "Save a Complete Simulation",hotkey="Ctrl+S")
        menu.AppendSeparator()
        menu.Append("&Run/Pause", self.Run_Pause, "Run a Simulation",hotkey="Ctrl+P")
        menu.Append("Restart from Current State", self.Restart)
        menu.Append("Reset Simulation", self.Reset_Simulation,hotkey="Ctrl+R")
        menu.AppendSeparator()
        menu.Append("Export Figure...", self.Export, "Export the Screen")
        menu.Append("&Quit", self.Quit, "Quit",hotkey="Ctrl+Q")

        menubar.Append(menu, "&File")

        
        menu = Menu(self)
        menu.Append("&Simulation Parameters", self.Set_Simulation_Parameters)
        menu.Append("&Input Parameters",  self.Set_Input_Parameters)
        menu.Append("&Output Neuron Parameters", self.Set_Output_Parameters)
        menu.Append("&Weight Parameters", self.Set_Weight_Parameters)
        menu.AppendSeparator()
        menu.Append("&Display", self.Display)
        menu.Append("Make &New Input Files", self.Nop)
        menu.Append("Parameter Structure", self.Set_Parameter_Structure)
    
        menubar.Append(menu, "&Edit")

        menu=Menu(self)
        menu.Append("&Help", self.Nop)
        menu.Append("&About", self.About)
        menubar.Append(menu, "&Help")
        
        self.SetMenuBar(menubar)
        self.CreateStatusBar()


        
        

        
    def Display(self,event=None):

        self.canvas.Show(False)
        dlg = FileDialog(self, "Choose Display Module",default_dir=os.getcwd()+"/",
                        wildcard='Python Plot Files|plot*.py|All Files|*.*')
        result = dlg.ShowModal()
        dlg.Destroy()

        if result == 'ok':
            lfname = dlg.GetPaths()[0]
            modulename=os.path.splitext(os.path.split(lfname)[-1])[0]

            self.params['display_module']=modulename
            
            if os.path.exists(self.tmpfile):
                sim=zpickle.load(self.tmpfile)
                self.Plot(sim)
                
            
        self.canvas.Show(True)
            
        
        
    def About(self,event):

        win=AboutWindow()
        win.Show()
        

    def Nop(self,event):
        self.canvas.Show(False)
        dlg = MessageDialog(self, "Error","Function Not Implemented",icon='error')
        dlg.ShowModal()
        dlg.Destroy()
        self.canvas.Show(True)

    def Export(self,event=None):
        export_fig(self)
    
    def Quit(self,event=None):
        
        if self.running:
            self.quitting=True
            self.stopping=True
            return
        
        self.canvas.Show(False)
        if self.modified:
            (root,sfname)=os.path.split(self.params['save_sim_file'])
            dlg=MessageDialog(self, 
                          text="Do you want to save the changes you made to %s?" % sfname,
                          title="Quit", ok=0, yes_no=1,cancel=1)
            result=dlg.ShowModal()
            dlg.Destroy()
            
            if result == 'cancel':
                self.canvas.Show(True)
                return
            elif result == 'yes':
                self.Save_Simulation()

        
        self.Close()
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)


        
def run(lfname=None,params=None,use_splash=True):
    if use_splash:
        app1=Application(splash.SplashFrame)
        app1.Run()

    app = Application(MainFrame, title="Plasticity",lfname=lfname,
                params=params)
    app.Run()
    
    

if __name__ == '__main__':

    from optparse import OptionParser

    
    parser = OptionParser()
    parser.add_option( "--nosplash", 
                  action="store_false", dest="splash", default=True,
                  help="don't show the splash screen")
    (options, args) = parser.parse_args()


    if options.splash:
        app1=Application(splash.SplashFrame)
        app1.Run()

    if len(args)>=1:
        lfname=args[0]
    else:
        lfname=None

    run(lfname)
    
