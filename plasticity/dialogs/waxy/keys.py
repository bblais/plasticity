# keys.py

import wx

class keys:
    enter = wx.WXK_RETURN
    # 'return' is not valid; reserved word

    alt = wx.WXK_ALT
    control = ctrl = wx.WXK_CONTROL
    shift = wx.WXK_SHIFT

    f1 = F1 = wx.WXK_F1
    f2 = F2 = wx.WXK_F2
    f3 = F3 = wx.WXK_F3
    f4 = F4 = wx.WXK_F4
    f5 = F5 = wx.WXK_F5
    f6 = F6 = wx.WXK_F6
    f7 = F7 = wx.WXK_F7
    f8 = F8 = wx.WXK_F8
    f9 = F9 = wx.WXK_F9
    f10 = F10 = wx.WXK_F10
    f11 = F11 = wx.WXK_F11
    f12 = F12 = wx.WXK_F12

    insert = wx.WXK_INSERT
    delete = wx.WXK_DELETE
    home = wx.WXK_HOME
    end = wx.WXK_END

    up = cursor_up = wx.WXK_UP
    down = cursor_down = wx.WXK_DOWN
    left = cursor_left = wx.WXK_LEFT
    right = cursor_right = wx.WXK_RIGHT

    pageup = pgup = wx.WXK_PRIOR   # not: wx.WXK_PAGEUP
    pagedown = pgdown = pgdn = wx.WXK_NEXT # not: wx.WXK_PAGEDOWN

    tab = wx.WXK_TAB
    backspace = bsp = wx.WXK_BACK
    esc = escape = wx.WXK_ESCAPE

    # XXX more later...?

