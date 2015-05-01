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
        
        
        b = Button(self, "MultiChoice Dialog",self.MultiChoice,default=True)
        self.AddComponent(b,border=10)
        
        
        self.Pack()
        self.SetSize((640, 480))

        
    def MultiChoice(self,event):
        
        
        lst = [ 'apple', 'pear', 'banana', 'coconut', 'orange', 'grape', 'pineapple',
                'blueberry', 'raspberry', 'blackberry', 'snozzleberry',
                'etc', 'etc..', 'etc...' ]

        dlg = MultiChoiceDialog( self, lst,
                                   "Pick some fruit from\nthis list",
                                   "MultiChoiceDialog")


        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenItems()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
        
    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="MultiChoiceDialog")
    app.Run()
