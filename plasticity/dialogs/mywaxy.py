from waxy import *
import waxy

import waxy.containers as containers
import waxy.styles as styles
import  wx.lib.scrolledpanel as scrolled

from wx import MilliSleep
from wx import EmptyImage

import string
from math import *

def Error(msg,parent=None):
    
    dlg = MessageDialog(parent, "Error",
            msg,icon='error')
    dlg.ShowModal()
    dlg.Destroy()

##class ImagePanel(Panel):
##
##    def __init__(self,parent,image=None,size=(200,200)):
##    
##        Panel.__init__(self,parent,size=size)
##       
##        self.image=image
##        
##        self.bitmap=Bitmap(self,image.ConvertToBitmap())
##        self.update()
##
##    def SetImage(self,image):
##        self.image=image
##        self.update()
##
##    def update(self):
##    
##        size=self.GetSizeTuple()
##        imsize=(self.image.GetWidth(),self.image.GetHeight())
##        
##        if (float(imsize[0])/float(size[0]))>(float(imsize[1])/float(size[1])):
##            scale=(float(imsize[0])/float(size[0]))
##        else:
##            scale=(float(imsize[1])/float(size[1]))
##            
##        newsize=(int(imsize[0]/scale),int(imsize[1]/scale))
##        newpos=( (size[0]-newsize[0])/2, (size[1]-newsize[1])/2)
##        self.bitmap.SetBitmap(self.image.Rescale(newsize[0],newsize[1]).ConvertToBitmap())
##        self.bitmap.SetPosition(newpos);        

class ScrollPanel(scrolled.ScrolledPanel, containers.Container):
    """ Sub-level containers inside a frame, used for layout. """
    def __init__(self, parent, direction="H", size=None, **kwargs):
        style = 0
        style |= styles.window(kwargs)
        scrolled.ScrolledPanel.__init__(self, parent, wx.NewId(), size=size or (-1,-1),
         style=style)

        self.BindEvents()
        self._create_sizer(direction)
        styles.properties(self, kwargs)
        self.Body()

class IntegerInputDialog(TextEntryDialog):
    
    def __init__(self, parent, title='Enter some text', 
                 prompt='Enter some text', default=None, cancel_button=1):
                     
        TextEntryDialog.__init__(self, parent, title=title,
                 prompt=prompt, default=str(default), 
                 cancel_button=cancel_button)


    def GetValue(self):
        
        try:
            val=TextEntryDialog.GetValue(self)
        except ValueError:
            return None
        
        try:
            int_val=eval("int("+val+")")
        except (SyntaxError,NameError):
            int_val=None
        
        return int_val
        
        
    def OnCharHook(self, event):
        key = event.KeyCode()

        if key == wx.WXK_ESCAPE:
            self.OnClickCancelButton()
            
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        
        good_chars=string.digits+'+*-()'
        if chr(key) in good_chars:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return
    
    
    
    def Validate(self):
        val = TextEntryDialog.GetValue(self)  # make sure the get a string
    
        good_chars=string.digits+'+*-()'
        for x in val:
            if x not in good_chars:
                return False
        
        try:
            int_val=eval("int("+val+")")
        except (SyntaxError,NameError):
            Error("Syntax Error")
            return False

        return True
    

def Input_Integer(title,
                 prompt, default=None,parent=None):
                     

    a=IntegerInputDialog(parent,title,prompt,default)
    result=a.ShowModal()
    
    if result=='ok':
        r=a.GetValue()
    else:
        r=None
        
    a.Destroy()

    return r
    
    
class FloatInputDialog(TextEntryDialog):
    
    def __init__(self, parent, title='Enter some text', 
                 prompt='Enter some text', default=None, cancel_button=1):
                     
        TextEntryDialog.__init__(self, parent, title=title,
                 prompt=prompt, default=str(default), 
                 cancel_button=cancel_button)


    def GetValue(self):

        try:
            val=TextEntryDialog.GetValue(self)
        except ValueError:
            return None
        
        try:
            float_val=eval("float("+val+")")
        except SyntaxError:
            float_val=None
        
        return float_val
        
        
    
    def Validate(self):
        val = TextEntryDialog.GetValue(self)  # make sure the get a string
    
        try:
            float_val=eval("float("+val+")")
        except (SyntaxError,NameError):
            Error("Syntax Error")
            return False

        return True
    
    

def Input_Float(title,
                 prompt, default=None,parent=None):
                     

    a=FloatInputDialog(parent,title,prompt,default)
    result=a.ShowModal()
    
    if result=='ok':
        r=a.GetValue()
    else:
        r=None
        
    a.Destroy()

    return r
    
    
class MainFrame(Frame):

    
    def Body(self):
        
        
        res=Input_Integer('this is the title','some text',5)
        print res
        self.Close()
    
if __name__ == '__main__':

    app = Application(MainFrame, title="Test")
    app.Run()
