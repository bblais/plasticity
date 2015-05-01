import wx
import waxyobject
from font import Font

# would be nice with a select all or something

class MultiChoiceDialog(wx.MultiChoiceDialog, waxyobject.WaxyObject):

    def __init__(self, parent,lst,text='Choose',title='Multi Choice Dialog'):
        wx.MultiChoiceDialog.__init__(self, parent,text,title,lst)

        self.lst=lst
        
    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.MultiChoiceDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

    def GetChosenItems(self):
        selections = self.GetSelections()
        strings = [self.lst[x] for x in selections]
        
        return strings

    
        
