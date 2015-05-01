# font.py

import wx

class Font(wx.Font):
    def __init__(self, name, size, italic=0, bold=0, underline=0):
        wx.Font.__init__(self, size, wx.DEFAULT, italic and wx.ITALIC or wx.NORMAL,
         bold and wx.BOLD or wx.NORMAL, underline, name)

    def IsItalic(self):
        return bool(self.GetStyle() & wx.ITALIC)

    def IsBold(self):
        return bool(self.GetWeight() & wx.BOLD)

    def IsUnderlined(self):
        return self.GetUnderlined()

