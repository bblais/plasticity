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
        
        
        b = Button(self, "Message Dialog: Question",self.Message,default=True)
        self.AddComponent(b,border=10)
        
        b = Button(self, "Choose Message: Statement",self.Message2)
        self.AddComponent(b,border=10)
        
        
        panel=Panel(self,direction='h')
        
        choices = MessageDialog._icons.keys()
        choices.sort()

        self.dd = DropDownBox(panel, choices)
        panel.AddComponent(self.dd, border=10)

        b = Button(panel, "Show message", self.Message3)
        panel.AddComponent(b,border=10)



        panel.Pack()
        

        self.AddComponent(panel,border=20)

        b = Button(self, "File Exists", self.Message4)
        self.AddComponent(b,border=10)
        
        self.Pack()
        self.SetSize((640, 480))

        
    def Message(self,event):

        dlg=MessageDialog(self,title="Holy cow", text="You wanna dance?",
              ok=0, yes_no=1)
        res=dlg.ShowModal()
        
        print res

        dlg.Destroy()
        
    def Message2(self,event):

        dlg=MessageDialog(self,text="Resistance is futile.")
        res=dlg.ShowModal()
        
        print res

        dlg.Destroy()
        
        
    def Message3(self,event):
        
        choice = self.dd.GetStringSelection()
        dlg = MessageDialog(self, "A message", "You chose: " + repr(choice),
              icon=choice)
        res=dlg.ShowModal()
        
        print res
        
        dlg.Destroy()
        
    def Message4(self,event):
        filename='hello.txt'
        dlg = MessageDialog(self, '"%s" already exists. Do you want to replace it?' % filename,
        'A file or folder with the same name already exists in plasticity. Replacing it will overwrite its current contents.',icon='Warning',cancel=1)
        result = dlg.ShowModal()

        print result
        
        dlg.Destroy()        

    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="MessageDialog")
    app.Run()
