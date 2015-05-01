# choosedirectory.py

import wx
import waxyobject

class DirectoryDialog(wx.DirDialog, waxyobject.WaxyObject):

    def __init__(self, parent, title="Choose a directory", new_dir_button=0):
        style = wx.DD_DEFAULT_STYLE
        if new_dir_button:
            style |= wx.DD_NEW_DIR_BUTTON
        wx.DirDialog.__init__(self, parent, title, style=style)

    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.DirDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'

    def GetChosenDirectory(self):
        """ Shorthand... """
        path = self.GetPath()
        return path
        
        
# EXPERIMENTAL:
# This dialog returns a list of filenames (dlg.GetPath()) upon success, and
# an empty list upon cancel.

def ChooseDirectory(parent, title="Choose a directory", new_dir_button=0):
    path = None
    dlg = DirectoryDialog(parent, title=title, new_dir_button=new_dir_button)
    if dlg.ShowModal() == 'ok':
        path = dlg.GetPath()
    dlg.Destroy()
    return path

