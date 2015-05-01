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
        
        
        b = Button(self, "About Box1",self.About1,default=True)
        self.AddComponent(b)
        
        b = Button(self, "About Box2",self.About2,default=True)
        self.AddComponent(b)
        
        self.Pack()
        self.SetSize((640, 480))

        
    def About1(self,event):
        
        licenseText = "blah " * 250 + "\n\n" +"yadda " * 100
        
        AboutBox(self,name='Hello World',
                 version='1.2.3',
                 copyright="(C) 2006 Programmers and Coders Everywhere",
                 description=(
            "A \"hello world\" program is a software program that prints out "
            "\"Hello world!\" on a display device. It is used in many introductory "
            "tutorials for teaching a programming language."
            
            "\n\nSuch a program is typically one of the simplest programs possible "
            "in a computer language. A \"hello world\" program can be a useful "
            "sanity test to make sure that a language's compiler, development "
            "environment, and run-time environment are correctly installed."),
            url="http://en.wikipedia.org/wiki/Hello_world",
            webtitle="Hello World home page",
            developers=[ "Joe Programmer",
                            "Jane Coder",
                            "Vippy the Mascot" ],
            license=licenseText)
        
        
    def About2(self,event):
        
        licenseText = "blah " * 250 + "\n\n" +"yadda " * 100
        
        info={}
        info['name']='Hello World'
        info['version']='1.2.3'
        info['copyright']="(C) 2006 Programmers and Coders Everywhere"
        info['description']=(
            "A \"hello world\" program is a software program that prints out "
            "\"Hello world!\" on a display device. It is used in many introductory "
            "tutorials for teaching a programming language."
            
            "\n\nSuch a program is typically one of the simplest programs possible "
            "in a computer language. A \"hello world\" program can be a useful "
            "sanity test to make sure that a language's compiler, development "
            "environment, and run-time environment are correctly installed.")
        info['url']="http://en.wikipedia.org/wiki/Hello_world"
        info['webtitle']="Hello World home page"
        info['developers']=[ "Joe Programmer",
                            "Jane Coder",
                            "Vippy the Mascot" ]
        info['license']=licenseText
        
        
        AboutBox(self,info)
        
        
        

    def CloseWindow(self,event):
        self.Close()

if __name__=="__main__":
    app = Application(MainFrame, title="AboutBox")
    app.Run()
