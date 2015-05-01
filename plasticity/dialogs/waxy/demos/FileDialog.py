#!/usr/bin/env python

from waxy import *

wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"

class MainFrame(Frame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        b = Button(self, "File OPEN Dialog",self.File1,default=True)
        self.AddComponent(b,border=10)
        
        b = Button(self, "File SAVE Dialog",self.File2)
        self.AddComponent(b,border=10)
        
        b = Button(self, "File MULTIPLE OPEN Dialog",self.File3)
        self.AddComponent(b,border=10)
        
        b = Button(self, "File Dialog (default?)",self.File0)
        self.AddComponent(b,border=10)
        
        
        self.Pack()
        self.SetSize((640, 480))

        
    def File1(self,event):
        
        
        dlg=FileDialog(self,wildcard=wildcard,open=True)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenFile()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def File2(self,event):
        
        
        dlg=FileDialog(self,wildcard=wildcard,save=True)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenFile()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def File3(self,event):
        
        
        dlg=FileDialog(self,wildcard=wildcard,open=True,multiple=True)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenFile()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def File0(self,event):
        
        
        dlg=FileDialog(self,wildcard=wildcard)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenFile()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="FileDialog")
    app.Run()
