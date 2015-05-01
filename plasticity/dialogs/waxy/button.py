# button.py

import containers
import waxyobject
import wx
import styles


class Button(wx.Button, waxyobject.WaxyObject):

    __events__ = {
        'Click': wx.EVT_BUTTON,
    }

    def __init__(self, parent, text="", event=None, size=None,
                        tooltip="", default=False, disabled=False, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.Button.__init__(self, parent, wx.NewId(), text, size=size or (-1,-1),
         style=style)

        self.BindEvents()
        if event:
            self.OnClick = event

        if tooltip:
            self.SetToolTipString(tooltip)
            
        if default:
            self.SetDefault()
            
        if disabled:
            self.Enable(False)
            
        styles.properties(self, kwargs)

    #
    # style parameters
    
    __styles__ = {
        'align': ({
            "left": wx.BU_LEFT,
            "right": wx.BU_RIGHT,
            "bottom": wx.BU_BOTTOM,
            "top": wx.BU_TOP,
            "exact": wx.BU_EXACTFIT,
        }, styles.DICTSTART),
        'flat': (wx.NO_BORDER, styles.NORMAL), 
          # seems to have no effect on Windows XP
        'exactfit': (wx.BU_EXACTFIT, styles.NORMAL),
    }

