# label.py

import wx
import containers
import waxyobject
import styles

class Label(wx.StaticText, waxyobject.WaxyObject):

    def __init__(self, parent, text="", size=None, **kwargs):
        #assert isinstance(parent, containers.Container)

        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.StaticText.__init__(self, parent, wx.NewId(), text,
         size=size or (-1,-1), style=style)
        styles.properties(self, kwargs)

    #
    # style parameters

    __styles__ = {
        'align': ({
            'left': wx.ALIGN_LEFT,
            'right': wx.ALIGN_RIGHT,
            'center': wx.ALIGN_CENTRE,
            'centre': wx.ALIGN_CENTRE,
        }, styles.DICTSTART),
        'noresize': (wx.ST_NO_AUTORESIZE, styles.NORMAL),
    }
    
