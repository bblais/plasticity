# frame.py

import wx
import containers
import styles

class Frame(wx.Frame, containers.Container):
    """ Top-level frame (window) with built-in sizer. """

    __events__ = {
        'Close': wx.EVT_CLOSE,
        'Iconize': wx.EVT_ICONIZE,
        'Show': wx.EVT_SHOW,
        'Activate': wx.EVT_ACTIVATE,
        'Idle': wx.EVT_IDLE,
        # some of these might be better off in events.py?

        'MenuHighlight': wx.EVT_MENU_HIGHLIGHT,
    }

    def __init__(self, parent=None, title="", direction="H", size=None, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.Frame.__init__(self, parent, wx.NewId(), title, size=size or (-1,-1),
         style=style)

        self.BindEvents()

        self._create_sizer(direction)
        styles.properties(self, kwargs)
        self.Body()

    def SetIcon(self, obj):
        """ Like wx.Frame.SetIcon, but also accepts a path to an icon file. """
        if isinstance(obj, str) or isinstance(obj, unicode):
            obj = wx.Icon(obj, wx.BITMAP_TYPE_ICO)    # FIXME
        wx.Frame.SetIcon(self, obj)

    #
    # style parameters

    def _params(self, kwargs):
        flags = wx.DEFAULT_FRAME_STYLE

        # REMOVE this flag if resize=0:
        flags &= ~(styles.styleboolexclude('resize', wx.RESIZE_BORDER, kwargs, reverse=1))
        flags &= ~(styles.styleboolexclude('close_box', wx.CLOSE_BOX, kwargs, reverse=1))
        flags &= ~(styles.styleboolexclude('minimize_box', wx.MINIMIZE_BOX, kwargs, reverse=1))
        flags &= ~(styles.styleboolexclude('maximize_box', wx.MAXIMIZE_BOX, kwargs, reverse=1))

        flags |= styles.stylebool('shaped', wx.FRAME_SHAPED, kwargs)
        flags |= styles.stylebool('stayontop', wx.STAY_ON_TOP, kwargs)
        flags |= styles.stylebool('stay_on_top', wx.STAY_ON_TOP, kwargs)
        return flags



class HorizontalFrame(Frame):
    def __init__(self, parent=None, title="", *args, **kwargs):
        Frame.__init__(self, parent=parent, title=title, direction='h', *args, **kwargs)

class VerticalFrame(Frame):
    def __init__(self, parent=None, title="", *args, **kwargs):
        Frame.__init__(self, parent=parent, title=title, direction='v', *args, **kwargs)

