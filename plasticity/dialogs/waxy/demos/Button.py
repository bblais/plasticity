#!/usr/bin/env python

from waxy import *

class MainFrame(VerticalFrame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        b = Button(self, "Default Button",self.OnClick,default=True)
        self.AddComponent(b)
        
        b = Button(self, "Hello Again",self.OnClick,
                                 tooltip="This is a Hello button...")
        self.AddComponent(b)
        
        b = Button(self, "Flat Button?",self.OnClick,
                          tooltip="This button has a style flag of wx.NO_BORDER. On some platforms that will give it a flattened look.",flat=True)
        self.AddComponent(b)

        self.Pack()
        self.SetSize((640, 480))
        
    def OnClick(self,event):
        print "Click! (%d)\n" % (event.GetId())
        
    def CloseWindow(self,event):
        self.Close()
    
    
if __name__=="__main__":
    app = Application(MainFrame, title="Some buttons")
    app.Run()
