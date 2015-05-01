import wx
import waxyobject
from font import Font

# would be nice with a select all or something

class SingleChoiceDialog(wx.SingleChoiceDialog, waxyobject.WaxyObject):

    def __init__(self, parent,lst,text='Choose',title='Single Choice Dialog'):
        wx.SingleChoiceDialog.__init__(self, parent,text,title,lst)

        self.lst=lst
        
    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.SingleChoiceDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

    def GetChosenItem(self):
        s = self.GetStringSelection()
        
        
        return s

    
        
