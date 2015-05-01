# checkbox.py

import wx
import waxyobject
import styles

class CheckBox(wx.CheckBox, waxyobject.WaxyObject):

    __events__ = {
        'Check': wx.EVT_CHECKBOX,
    }


    def __init__(self, parent, text='', size=None, border=1, **kwargs):
        flags = 0
        if not border:
            flags |= wx.NO_BORDER
        # XXX not sure what border does... there doesn't seem to be a visible
        # difference?
        flags |= self._params(kwargs)
        flags |= styles.window(kwargs)

        wx.CheckBox.__init__(self, parent, wx.NewId(), text, None,
         size or (-1, -1), flags)

        self.BindEvents()
        styles.properties(self, kwargs)

    _3states = {
        'checked': wx.CHK_CHECKED,
        'unchecked': wx.CHK_UNCHECKED,
        'undetermined': wx.CHK_UNDETERMINED,
    }

    def Set3StateValue(self, state):
        for name, flag in self._3states.items():
            if name.startswith(state):
                wx.CheckBox.Set3StateValue(self, flag)
                break
        else:
            raise KeyError, "Unknown state: %s" % (state,)

    def Get3StateValue(self):
        value = wx.CheckBox.Get3StateValue(self)
        if value == wx.CHK_CHECKED:
            return 'checked'
        elif value == wx.CHK_UNCHECKED:
            return 'unchecked'
        elif value == wx.CHK_UNDETERMINED:
            return 'undetermined'
        else:
            return '?'

    #
    # style parameters

    _checkbox_states = {
        2: wx.CHK_2STATE,
        3: wx.CHK_3STATE,
    }

    _checkbox_align = {
        'left': 0,
        'right': wx.ALIGN_RIGHT,
    }

    def _params(self, kwargs):
        flags = 0
        flags |= styles.styledict('states', self._checkbox_states, kwargs, wx.CHK_2STATE)
        flags |= styles.styledictstart('align', self._checkbox_align, kwargs, 0)
        return flags
