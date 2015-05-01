# notebook.py

import waxyobject
import wx
import styles
import utils

class NoteBook(wx.Notebook, waxyobject.WaxyObject):

    __events__ = {
        'PageChanging': wx.EVT_NOTEBOOK_PAGE_CHANGING,
        'PageChanged': wx.EVT_NOTEBOOK_PAGE_CHANGED,
    }

    def __init__(self, parent, size=(640,480), **kwargs):

        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        self.id = wx.NewId()
        wx.Notebook.__init__(self, parent, self.id, style=style, size=size)
        self.BindEvents()
        styles.properties(self, kwargs)

#    def AddPage(self, window, *args, **kwargs):
#        wx.Notebook.AddPage(self, window, *args, **kwargs)

    def GetCurrentPage(self):
        idx = self.GetSelection()
        if idx == -1:
            raise ValueError, "NoteBook currently has no pages"
        else:
            return self.GetPage(idx)

    #
    # style parameters

    _notebook_orientation = {
        "left": wx.NB_LEFT,
        "right": wx.NB_RIGHT,
        "bottom": wx.NB_BOTTOM,
        "top": 0,
    }

    def _params(self, kwargs):
        flags = 0
        flags |= styles.styledictstart('orientation', self._notebook_orientation, kwargs)
        flags |= styles.stylebool('fixedwidth', wx.NB_FIXEDWIDTH, kwargs)
        flags |= styles.stylebool('multiline', wx.NB_MULTILINE, kwargs)
        return flags
