# menu.py

import wx
import waxyobject
import string

class Menu(wx.Menu, waxyobject.WaxyObject):

    def __init__(self, parent, autoevents=1):
        wx.Menu.__init__(self)
        self.parent = parent    # necessary for hooking up events
        self.autoevents = autoevents

    def Append(self, title, event=None, tooltip="", type="", hotkey=""):
        # Note: the order is different from wx.Menu.Append!
        style = 0
        style |= {
            "r": wx.ITEM_RADIO,
            "c": wx.ITEM_CHECK,
        }.get(type.lower()[:1], wx.ITEM_NORMAL)

        if hotkey:
            title = title + "\t" + hotkey

        id = wx.NewId()
        item = wx.Menu.Append(self, id, title, tooltip, style)
        if event:
            # you *can* choose to specify no event, but that doesn't seem very
            # useful
            wx.EVT_MENU(self.parent, id, event)
        elif self.autoevents:
            wx.EVT_MENU(self.parent, id, self.HandleAutoEvent)

        return item

    def AppendMenu(self, title, menu):
        id = wx.NewId()
        return wx.Menu.AppendMenu(self, id, title, menu)
        # I suppose there's room for an event here, but why bother...?

    def GetItem(self, title):
        """ Find item by title, bypassing the internal id. """
        id = self.FindItem(title)
        item = self.FindItemById(id)
        return item

    def Delete(self, obj):
        # according to the wxWindows reference, wx.Menu.Delete() also accepts
        # MenuItems... but apparently that isn't true, at least not in wxPython.
        # So let's fix it:
        if isinstance(obj, wx.MenuItem):
            id = obj.GetId()
            return wx.Menu.Delete(self, id)
        else:
            # assume it's a number
            return wx.Menu.Delete(self, obj)

    def HandleAutoEvent(self, event):
        id = event.GetId()
        menuitem = self.FindItemById(id)

        def GetFullTitle(id):
            menubar = self.parent.GetMenuBar()
            if menubar:
                for mwitem in menubar.Walk():
                    if mwitem.items and mwitem.items[-1].GetId() == id:
                        title = mwitem.name
                        for menuitem in mwitem.items:
                            title = title + " " + menuitem.GetLabel()
                        return title
            return None

        title = GetFullTitle(id)
        if title:
            methodname = "Menu_" + genmethodname(title)
            #print "Looking for:", methodname
            if hasattr(self.parent, methodname):
                f = getattr(self.parent, methodname)
                f(event)

    # these aliases make sense...
    Add = Append
    AddMenu = AppendMenu

    def Walk(self):
        for menuitem in self.GetMenuItems():
            yield [menuitem]
            submenu = menuitem.GetSubMenu()
            if submenu:
                for subitem in submenu.Walk():
                    yield [menuitem] + subitem

    # TODO: Is it possible to write a better GetTitle() or GetRealTitle()
    # or something, that gives us the actual label of the menu?

class MenuBar(wx.MenuBar, waxyobject.WaxyObject):
    def __init__(self, parent=None, *args, **kwargs):
        wx.MenuBar.__init__(self, *args, **kwargs)
        if parent: parent.SetMenuBar(self)

    def Append(self, menu, text):
        wx.MenuBar.Append(self, menu, text)

    def Walk(self):
        for i in range(self.GetMenuCount()):
            menu = self.GetMenu(i)
            for items in menu.Walk():
                menuwalkitem = _MenuWalkItem()
                menuwalkitem.name = self.GetLabelTop(i)
                menuwalkitem.menu = menu
                menuwalkitem.items = items
                yield menuwalkitem

class _MenuWalkItem:
    pass

#
# auxiliary methods

def genmethodname(title):
    allowed = string.letters + string.digits + "_"
    name = ""
    for char in title:
        if char in allowed:
            name = name + char
        elif char == ' ':
            name = name + '_'
    return name

