# events.py

import wx

# place general events here... OnEnter, OnExit, mouse events, etc.

events = {
    'Enter': wx.EVT_ENTER_WINDOW,       # entering a control w/ mouse pointer
    'EnterWindow': wx.EVT_ENTER_WINDOW,
    'Exit': wx.EVT_LEAVE_WINDOW,        # leaving a control w/ mouse pointer
    'ExitWindow': wx.EVT_LEAVE_WINDOW,
    'GetFocus': wx.EVT_SET_FOCUS,       # control gets focus
    'HotKey': wx.EVT_HOTKEY,
    'KeyDown': wx.EVT_KEY_DOWN,
    'KeyUp': wx.EVT_KEY_UP,
    'Leave': wx.EVT_LEAVE_WINDOW,
    'LeaveWindow': wx.EVT_LEAVE_WINDOW,
    'LeftClick': wx.EVT_LEFT_DOWN,      # alias for LeftDown
    'LeftDown': wx.EVT_LEFT_DOWN,
    'LeftUp': wx.EVT_LEFT_UP,
    'LoseFocus': wx.EVT_KILL_FOCUS,     # control loses focus
    'Move': wx.EVT_MOVE,                # window is moved. is this for frames only?
    'Resize': wx.EVT_SIZE,              # same as 'Size'
    'RightClick': wx.EVT_RIGHT_DOWN,    # alias for RightDown
    'RightDown': wx.EVT_RIGHT_DOWN,
    'RightUp': wx.EVT_RIGHT_UP,
    'Size': wx.EVT_SIZE,                # window is resized

    # NOTE: OnPaint should really be here, but this causes problems with the
    # OnPaint method that many controls already have.
}
