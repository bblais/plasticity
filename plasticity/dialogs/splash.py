from waxy import *
from mywaxy import *
import sys
import os

class SplashFrame(Frame):
    
    def __init__(self,parent=None,title='',direction='H',
                    size=None,params=None):
        Frame.__init__(self,parent,title,direction,size,border='simple')

    
    def Body(self):
        self.base_dir=os.path.dirname(__file__)
        if not self.base_dir:
            self.base_dir='.'
         
        fname=self.base_dir+"/images/icon.png"
#        fname='icon.png'
        self.panel=Panel(self)
        b=Bitmap(self.panel,Image(fname).ConvertToBitmap())
        self.panel.AddComponent(b)
        self.panel.Pack()
        self.panel.Show()
        self.AddComponent(self.panel)
        self.Pack()
        self.CenterOnScreen()
        self.SetWindowStyle(border='simple')
        
    def OnIdle(self,event):
        MilliSleep(2000)
        self.MakeModal(False)
        self.Close()

        
