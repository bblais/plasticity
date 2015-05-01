# dialog.py

# TODO: Pressing Esc in a dialog should be the same as Cancel...
# (but how?  using EVT_CHAR doesn't work...  neither does OnCharHook.)

import wx

from button import Button
from containers import Container
from line import Line
from panel import Panel
from keys import keys
import frame

# TODO: styles (same as Frame?)

class Dialog(wx.Dialog, Container):

    __events__ = frame.Frame.__events__.copy()
    __events__ .update({
        'CharHook': wx.EVT_CHAR_HOOK,
    })

    def __init__(self, parent, title, cancel_button=1):
        wx.Dialog.__init__(self, parent, wx.NewId(), title, wx.DefaultPosition)

        # this should create self.sizer and give access to self.AddComponent
        self._create_sizer('vertical')

        # enter stuff here...
        self.Body()

        # add line and buttons pane...
        line = Line(self, size=(20,-1), direction='horizontal')
        self.AddComponent(line, align='center', stretch=1, border=5)

        panel = self.AddButtonPanel(cancel_button)

        self.BindEvents()

        panel.Pack()
        self.AddComponent(panel)

        self.Pack()

        self.Centre()

    def AddButtonPanel(self, cancel_button=1):
        panel = Panel(self, direction='horizontal')
        self.okbutton = Button(panel, "OK", event=self.OnClickOKButton)
        self.okbutton.SetDefault()
        panel.AddComponent(self.okbutton, expand=1, border=5)

        if cancel_button:
            cancelbutton = Button(panel, "Cancel", event=self.OnClickCancelButton)
            panel.AddComponent(cancelbutton, expand=1, border=5)
        return panel

    def OnClickOKButton(self, event=None):
        if self.Validate():
            event.Skip()
            # only close the dialog if we validate:
            self.EndModal(wx.ID_OK)
        else:
            self.OnValidateError(event)

    def OnClickCancelButton(self, event=None):
        self.EndModal(wx.ID_CANCEL)

    def OnValidateError(self, event=None):
        """ Override this to take action when the input does not validate.
            (E.g. display an error message, etc.) """

    def ShowModal(self):
        """ Show the dialog modally.  Returns 'ok' or 'cancel'. """
        r = wx.Dialog.ShowModal(self)
        return {
            wx.ID_OK: "ok",
            wx.ID_CANCEL: "cancel",
        }.get(r, "?")

    def Body(self):
        # override this
        # NOTE: do not call self.Pack() here, it's called automatically later
        return None

    def Validate(self):
        """ Override this to validate input and return 0 if it's not correct.
            Return 1 otherwise. """
        return 1

    # this doesn't work -- or does it?:
    def OnCharHook(self, event=None):
        if event.GetKeyCode() == keys.esc:
            self.OnClickCancelButton()
        event.Skip()


def showdialog(dialogclass, *args, **kwargs):
    """ Easy function to call dialogs and clean up when it's done. """
    dlg = dialogclass(*args, **kwargs)
    try:
        result = dlg.ShowModal()
    finally:
        dlg.Destroy()
    return result

