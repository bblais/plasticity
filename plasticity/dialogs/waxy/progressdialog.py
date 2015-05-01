# progressdialog.py

import wx
import waxyobject

class ProgressDialog(wx.ProgressDialog, waxyobject.WaxyObject):

    def __init__(self,parent=None,title="Progress", message="Progress", 
                  maximum=100,abort=1,modal=1,show_elapsed_time=1,show_remaining_time=1):
        style = 0
        if abort:
            style |= wx.PD_CAN_ABORT
        if modal:
            style |= wx.PD_APP_MODAL
        if show_elapsed_time:
            style |= wx.PD_ELAPSED_TIME
        if show_remaining_time:
            style |= wx.PD_REMAINING_TIME
        wx.ProgressDialog.__init__(self, title, message,
                        maximum, parent,style)

    def ShowModal(self):
        """ Simplified ShowModal(), returning strings 'ok' or 'cancel'. """
        result = wx.ProgressDialog.ShowModal(self)
        if result == wx.ID_OK:
            return 'ok'
        else:
            return 'cancel'
