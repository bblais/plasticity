# messagedialog.py

import wx
import waxyobject
import core

class MessageDialog(wx.MessageDialog, waxyobject.WaxyObject):
    """Displays a message dialog.  Title, text, buttons (OK/Cancel/Yes/No),
       and icon are configurable.
    """

    _icons = {
        'asterisk': wx.ICON_ASTERISK,
        'error': wx.ICON_ERROR,
        'exclamation': wx.ICON_EXCLAMATION,
        'hand': wx.ICON_HAND,
        'information': wx.ICON_INFORMATION,
        'mask': wx.ICON_MASK,
        'question': wx.ICON_QUESTION,
        'stop': wx.ICON_STOP,
        'warning': wx.ICON_WARNING,
    }

    def __init__(self, parent, title="Message", text="A message", ok=0,
                 cancel=0, yes_no=0, icon=""):
        style = 0
        if ok: style |= wx.OK
        if cancel: style |= wx.CANCEL
        if yes_no: style |= wx.YES_NO

        # set icon... some of these values show the same icon, at least on
        # Windows.
        icon = self._icons.get(icon.lower(), None)
        if icon:
            style |= icon

        # use a sensible default
        if not (ok or cancel or yes_no):
            style |= wx.OK

        wx.MessageDialog.__init__(self, parent, text, title, style)

    def ShowModal(self):
        r = wx.MessageDialog.ShowModal(self)
        return {
            wx.ID_OK: 'ok',
            wx.ID_CANCEL: 'cancel',
            wx.ID_YES: 'yes',
            wx.ID_NO: 'no',
        }.get(r, "?")


def ShowMessage(title, text, icon=""):
    """ Displays a message with an OK button.  A bit like Delphi's ShowMessage
        procedure. """
    parent = core.GetActiveWindow()
    dlg = MessageDialog(parent, title, text, ok=1, icon=icon)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()

