# panel.py

import wx
import containers
import styles

class Panel(wx.Panel, containers.Container):
    """ Sub-level containers inside a frame, used for layout. """
    def __init__(self, parent, direction="H", size=None, **kwargs):
        style = 0
        style |= styles.window(kwargs)
        wx.Panel.__init__(self, parent, wx.NewId(), size=size or (-1,-1),
         style=style)

        self.BindEvents()
        self._create_sizer(direction)
        styles.properties(self, kwargs)
        self.Body()

class HorizontalPanel(Panel):
    def __init__(self, parent, **kwargs):
        Panel.__init__(self, parent, direction='h', **kwargs)

class VerticalPanel(Panel):
    def __init__(self, parent, **kwargs):
        Panel.__init__(self, parent, direction='v', **kwargs)

