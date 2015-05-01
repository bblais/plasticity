# dropdownbox.py

# todo: styles... if any?

import wx
import containers
import waxyobject
import styles

class DropDownBox(wx.Choice, waxyobject.WaxyObject):

    __events__ = {
        'Select': wx.EVT_CHOICE,
    }

    def __init__(self, parent, choices=[], size=None, **kwargs):
        style = 0
        style |= styles.window(kwargs)
        wx.Choice.__init__(self, parent, wx.NewId(), choices=choices,
         size=size or (-1,-1), style=style)

        self.BindEvents()
        styles.properties(self, kwargs)

    def SetItems(self, items):
        """ Clear the internal list of items, and set new items.  <items> is
            a list of 2-tuples (string, data). """
        self.Clear()
        for s, data in items:
            self.Append(s, data)

    def GetItems(self):
        """ Return a list of 2-tuples (string, data). """
        items = []
        for i in range(self.GetCount()):
            s = self.GetString(i)
            data = self.GetClientData(i)
            items.append((s, data))
        return items

