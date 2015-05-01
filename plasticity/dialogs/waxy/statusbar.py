# statusbar.py

import wx
import waxyobject
import styles

class StatusBar(wx.StatusBar, waxyobject.WaxyObject):

    def __init__(self, parent, numpanels=1, add=1, **kwargs):
        # note: does not support the 'size' parameter
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.StatusBar.__init__(self, parent, wx.NewId(), style=style)

#        self.SetDefaultFont()
        self.SetFieldsCount(numpanels)
        if add:
            parent.SetStatusBar(self)

        self.BindEvents()
        styles.properties(self, kwargs)


    # allows for: statusbar[0] = "text"
    def __setitem__(self, index, text):
        self.SetStatusText(text, index)

    #
    # style parameters

    def _params(self, kwargs):
        flags = 0
        flags |= styles.stylebool('sizegrip', wx.ST_SIZEGRIP, kwargs)
        return flags

