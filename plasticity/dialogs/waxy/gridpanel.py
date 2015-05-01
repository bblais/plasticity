# gridpanel.py

# todo: styles

import wx
import containers
import panel

class GridPanel(wx.Panel, containers.GridContainer):
    """ Sub-level containers inside a frame, used for layout. """
    def __init__(self, parent=None, rows=3, cols=3, hgap=1, vgap=1):
        wx.Panel.__init__(self, parent or NULL, wx.NewId())

        self._create_sizer(rows, cols, hgap, vgap)
#        self.SetDefaultFont()
        self.Body()

'''
NOTES

1. Do not make the mistake of writing GridPanel(parent, 3, 3, 2, 2) or something
like that.  This will work, but set the *title* to 3, and cols to 2.
Why does a Panel need a title anyway?  Can we remove this?
'''
