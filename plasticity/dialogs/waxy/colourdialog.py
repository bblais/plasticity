import wx
import waxyobject
from font import Font

class ColourDialog(wx.ColourDialog, waxyobject.WaxyObject):

    def __init__(self, parent):
        wx.ColourDialog.__init__(self, parent)
        # Ensure the full colour dialog is displayed, 
        # not the abbreviated version.
        self.GetColourData().SetChooseFull(True)

    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.ColourDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

    def GetChosenColour(self):
        """ Shorthand... """
        data = self.GetColourData()
        color = data.GetColour().Get()
        return color

class ColorDialog(ColourDialog):
    
    
    def GetChosenColor(self):
        """ Shorthand... """
        data = self.GetColourData()
        color = data.GetColour().Get()
        return color
