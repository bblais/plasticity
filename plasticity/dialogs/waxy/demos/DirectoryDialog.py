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
        
        
        b = Button(self, "Directory Dialog",self.Directory,default=True)
        self.AddComponent(b,border=10)
        
        b = Button(self, "Choose Directory",self.Directory2)
        self.AddComponent(b,border=10)
        
        b = Button(self, "Directory Dialog with New Button",self.Directory3,default=True)
        self.AddComponent(b,border=10)
        
        
        self.Pack()
        self.SetSize((640, 480))

        
    def Directory(self,event):
        
        
        dlg=DirectoryDialog(self)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenDirectory()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def Directory2(self,event):
        
        
        res=ChooseDirectory(self)
        
        print "Chose: ",res


    def Directory3(self,event):
        
        
        dlg=DirectoryDialog(self,new_dir_button=True)
        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenDirectory()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="DirectoryDialog")
    app.Run()
