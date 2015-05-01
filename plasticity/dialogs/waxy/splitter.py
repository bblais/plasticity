# splitter.py

import wx
import waxyobject
import styles
import utils

class Splitter(wx.SplitterWindow, waxyobject.WaxyObject):

    __events__ = {
        'SashPosChanging': wx.EVT_SPLITTER_SASH_POS_CHANGING,
        'SashPosChanged': wx.EVT_SPLITTER_SASH_POS_CHANGED,
        'Unsplit': wx.EVT_SPLITTER_UNSPLIT,
        'DoubleClick': wx.EVT_SPLITTER_DCLICK,
    }

    def __init__(self, parent, size=None, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)
        wx.SplitterWindow.__init__(self, parent, wx.NewId(), style=style)

        if size:
            self.SetSize(size)

        self.BindEvents()
        styles.properties(self, kwargs)

        # I would have liked to add the windows to the constructor, but it's
        # not possible because the Splitter needs to be present as the
        # windows' parent... hmm...

    def Split(self, window1, window2, direction="horizontal", sashposition=100,
              minsize=20):

        if direction.lower().startswith("h"):
            self.SplitHorizontally(window1, window2, sashposition)
        elif direction.lower().startswith("v"):
            self.SplitVertically(window1, window2, sashposition)
        else:
            raise ValueError, "direction must be horizontal or vertical"

        self.SetMinimumPaneSize(minsize)

    #
    # style parameters

    def _params(self, kwargs):
        flags = 0
        flags |= styles.stylebool('permit_unsplit', wx.SP_PERMIT_UNSPLIT, kwargs)
        flags |= styles.stylebool('live_update', wx.SP_LIVE_UPDATE, kwargs)
        flags |= styles.stylebool('no_xp_theme', wx.SP_NO_XP_THEME, kwargs)
        flags |= styles.stylebool('border', wx.SP_BORDER, kwargs)
        flags |= styles.stylebool('sash3d', wx.SP_3DSASH, kwargs)
        flags |= styles.stylebool('all3d', wx.SP_3D, kwargs)
        return flags
