#!/usr/bin/env python

from waxy import *

class MyDialog(SingleChoiceDialog):
    
    def OnClick(self):
        
        print "hello!"
        


class MainFrame(VerticalFrame): # frame has a sizer built in

    def Body(self):

        self.CenterOnScreen()

        self.CreateStatusBar()
        self.SetStatusText("This is the statusbar")

        menubar = MenuBar(self)
        menu1 = Menu(self)
        menu1.Append("E&xit", self.CloseWindow, "Exit demo",hotkey="Ctrl+Q")
        menubar.Append(menu1, "&File")
        
        
        b = Button(self, "SingleChoice Dialog",self.SingleChoice,default=True)
        self.AddComponent(b,border=10)
        
        b = Button(self, "Custom SingleChoice Dialog",self.SingleChoice2)
        self.AddComponent(b,border=10)
        
        
        self.Pack()
        self.SetSize((640, 480))

        
    def SingleChoice(self,event):
        
        
        lst = [ 'apple', 'pear', 'banana', 'coconut', 'orange', 'grape', 'pineapple',
                'blueberry', 'raspberry', 'blackberry', 'snozzleberry',
                'etc', 'etc..', 'etc...' ]

        dlg = SingleChoiceDialog( self, lst,
                                   "Pick some fruit from\nthis list",
                                   "SingleChoiceDialog")


        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenItem()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
    def SingleChoice2(self,event):
        
        
        lst = [ 'apple', 'pear', 'banana', 'coconut', 'orange', 'grape', 'pineapple',
                'blueberry', 'raspberry', 'blackberry', 'snozzleberry',
                'etc', 'etc..', 'etc...' ]

        dlg = MyDialog( self, lst,
                                   "Pick some fruit from\nthis list",
                                   "SingleChoiceDialog")


        res=dlg.ShowModal()
        
        if res=='ok':
            print "Ok: ",dlg.GetChosenItem()
            
        else:
            print "Canceled!"
            
        dlg.Destroy()
        
        
    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="SingleChoiceDialog")
    app.Run()
