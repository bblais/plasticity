#!/usr/bin/env python

from dialogs.waxy import *
#from waxy import *

import os,sys
import glob
from run_sim import Plot

    
class MainFrame(Frame):

    def __init__(self,parent=None,title='',direction='v',
                    size=(200,800),default_wildcard=None):

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
        
        files=glob.glob(wildcard)
        
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
            self.UpdateWindowUI()
            self.Refresh()
            
            Plot(file)
            self.SetCursor('default')
        
        
    def CloseWindow(self,event):
        self.Close()
        
def run(default_wildcard=None):
    app = Application(MainFrame, title="Plot Sims",default_wildcard=default_wildcard)
    app.Run()

    
if __name__ == '__main__':

    if len(sys.argv)>1:
        default_wildcard=sys.argv[1]
    else:
        default_wildcard=None

    run(default_wildcard)

