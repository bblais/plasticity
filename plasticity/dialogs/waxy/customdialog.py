# customdialog.py

import wx
import containers
import dialog

class CustomDialog(wx.Dialog, containers.Container):

    __events__ = dialog.Dialog.__events__.copy()

    def __init__(self, parent, title=""):
        wx.Dialog.__init__(self, parent, wx.NewId(), title, wx.DefaultPosition)

        # this should create self.sizer and give access to self.AddComponent
        self._create_sizer('vertical')

        # We use EndModal() internally, and that requires that we return
        # IDs.  _modalhooks is a mapping from ID to desired return value (as a
        # string), used by CustomDialog.ShowModal.  _count is used for
        # generating the unique IDs.
        self._modalhooks = {}
        self._count = 0 # enumerator

        self.Body()

        self.BindEvents()
        self.Pack()
        self.Centre()

    def Body(self):
        pass

    def _GetEnumValue(self):
        self._count = self._count + 1
        return self._count

    def SetBehavior(self, button, result, validator=None, event=None):
        """ Set the behavior for the given button.  <result> is the desired
            result, as a string ('ok', 'cancel', 'foo', etc).  <event> is
            called, if defined.
            Note 1: EndModal() is always called, causing the dialog to be
            closed.  If you don't want this (i.e. if you want a "regular" button
            on the dialog), don't call SetBehavior.
            Note: Any OnClick-event that already exists on the button will
            be overwritten.  It will *not* be called.
        """
        id = self._GetEnumValue()
        self._modalhooks[id] = result
        def OnClick(zevent):
            # XXX there's room for a "validator" here
            if validator:
                pass # not sure how to do this yet
            if event:
                event(zevent)
                # note: if an exception occurs here, it is not caught
            self.EndModal(id)
        button.OnClick = OnClick

    def OnClickButton(self, event):
        button = event.GetEventObject()

    def ShowModal(self):
        r = wx.Dialog.ShowModal(self)
        # here, we need to figure out which button was clicked!
        return self._modalhooks.get(r, "?")

