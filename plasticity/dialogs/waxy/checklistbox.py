# checklistbox.py
# XXX doesn't work on Mac.

# todo: styles (if any)

import wx
import waxyobject
import styles

class CheckListBox(wx.CheckListBox, waxyobject.WaxyObject):

    __events__ = {
        'CheckListBox': wx.EVT_CHECKLISTBOX,
    }

    def __init__(self, parent, choices=[], size=None, **kwargs):
        style = 0
        #style |= checklistbox_params(kwargs)
        style |= styles.window(kwargs)

        wx.CheckListBox.__init__(self, parent, wx.NewId(), choices=choices, style=style)

        self.BindEvents()

        styles.properties(self, kwargs)


