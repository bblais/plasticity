from waxy import *

HTML="""<html>
               <center><b>Plasticity for Python</b><center>
<ul>
<li>        Written by Brian Blais
<li>        Uses Wax (<a href="http://sourceforge.net/projects/waxgui">http://sourceforge.net/projects/waxgui</a>)
</ul>
</html>
"""

class AboutWindow(Frame):
    def Body(self):
        self.htmlwindow = HTMLWindow(self)
        self.AddComponent(self.htmlwindow, expand='both')
        self.htmlwindow.SetPage(HTML)
        self.Pack()
        self.Size = (500, 300)
        self.CenterOnScreen()
        self.MakeModal(True)
        
    def OnClose(self,event):
        self.MakeModal(False)
        event.Skip()
