# filedialog.py

import wx
import waxyobject

class FileDialog(wx.FileDialog, waxyobject.WaxyObject):

    def __init__(self, parent, title="Choose a file", default_dir="",
                 default_file="", wildcard="*.*", open=0, save=0, multiple=0):
        style = 0
        if open:
            style |= wx.OPEN
        elif save:
            style |= wx.SAVE
            style |= wx.OVERWRITE_PROMPT
        if multiple:
            style |= wx.MULTIPLE

        self.multiple=multiple
            
        wx.FileDialog.__init__(self, parent, title, default_dir, default_file,
         wildcard, style)

    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.FileDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

        
    def GetChosenFile(self):
        """ Shorthand... """
        data = self.GetPaths()
        
        if not self.multiple:
            data=data[0]
        
        return data
