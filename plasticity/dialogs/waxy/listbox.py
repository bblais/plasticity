# listbox.py

import wx
import containers
import waxyobject
import styles

class ListBox(wx.ListBox, waxyobject.WaxyObject):

    __events__ = {
        'Click': wx.EVT_LISTBOX,
        'DoubleClick': wx.EVT_LISTBOX_DCLICK,
    }

    def __init__(self, parent, choices=[], size=None, **kwargs):
        style = 0
        style |= self._params(kwargs)
        style |= styles.window(kwargs)

        wx.ListBox.__init__(self, parent, wx.NewId(), size=size or (-1,-1),
         choices=choices, style=style)

        self.BindEvents()

        styles.properties(self, kwargs)

    def SetSelectionType(self, selection):
        style = 0
        selection = selection.lower()
        if selection == "single":
            style |= wx.LB_SINGLE
        elif selection == "multiple":
            style |= wx.LB_MULTIPLE
        elif selection == "extended":
            style |= wx.LB_EXTENDED
        else:
            raise ValueError, "selection must be single, multiple or extended"
        return style

    def SetItems(self, items):
        """ Clear the internal list of items, and set new items.  <items> is
            a list of 2-tuples (string, data). """
        self.Clear()
        for s, data in items:
            self.Append(s, data)

    def Fill(self, items):
        """ Like SetItems, but just uses a list of strings. """
        self.Clear()
        for s in items:
            self.Append(s)

    def GetItems(self):
        """ Return a list of 2-tuples (string, data). """
        items = []
        for i in range(self.GetCount()):
            s = self.GetString(i)
            data = self.GetClientData(i)
            items.append((s, data))
        return items

    # TODO:
    # Add __getitem__, __setitem__, __delitem__
    # These should probably work with tuples (string, data).
    # 1-tuples can be used, in which case data are left alone.
    # Non-tuples are not allowed.

    # We should also be able to iterate over a ListBox...
    # Although for (s, data) in listbox.GetItems() would work too.

    #
    # style parameters

    _listbox_selection = {
        'single': wx.LB_SINGLE,
        'multiple': wx.LB_MULTIPLE,
        'extended': wx.LB_EXTENDED,
    }

    _listbox_scrollbar = {
        'always': wx.LB_ALWAYS_SB,
        'needed': wx.LB_NEEDED_SB,
    }

    def _params(self, kwargs):
        flags = 0
        flags |= styles.styledictstart('selection', self._listbox_selection, kwargs)
        flags |= styles.styledictstart('scrollbar', self._listbox_scrollbar, kwargs)
        flags |= styles.stylebool('sort', wx.LB_SORT, kwargs)
        flags |= styles.stylebool('horizontal_scrollbar', wx.LB_HSCROLL, kwargs)

        return flags
