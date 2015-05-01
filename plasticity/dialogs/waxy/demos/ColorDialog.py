#!/usr/bin/env python

from waxy import *

class MainFrame(Frame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        b = Button(self, "Color Dialog",self.Color,default=True)
        self.AddComponent(b)
        
        
        self.Pack()
        self.SetSize((640, 480))

        
    def Color(self,event):
        
        
        dlg=ColorDialog(self)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenColor()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        


    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="ColorDialog")
    app.Run()
