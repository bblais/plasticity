# fontdialog.py

# Issues:
# objects' GetFont() really should return a Font instance, not a wx.Font

import wx
import waxyobject
from font import Font

class FontDialog(wx.FontDialog, waxyobject.WaxyObject):

    def __init__(self, parent, data=None):
        if not data:
            data = wx.FontData()
        wx.FontDialog.__init__(self, parent, data)

    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.FontDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

    def GetChosenFont(self):
        """ Shorthand... """
        data = self.GetFontData()
        font = data.GetChosenFont()
        font.__class__ = Font
        return font

# XXX
# Problem: GetFontData() returns a wxFontData object, whose GetChosenFont()
# still returns a wxFont, not a wax Font.  No big deal really, but inconsistent.
# Maybe Wax needs its own FontData class...?
