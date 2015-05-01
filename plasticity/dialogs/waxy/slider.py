# slider.py

import wx
import containers
import waxyobject
import styles

class Slider(wx.Slider, waxyobject.WaxyObject):
    __events__ = {
        'Click': wx.EVT_BUTTON,
    }
