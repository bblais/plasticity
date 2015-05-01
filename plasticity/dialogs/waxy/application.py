# application.py

import wx
import sys
#from waxconfig import WaxConfig
#import font

class Application(wx.App):
    def __init__(self, frameklass, *args, **kwargs):
        # takes a frame *class* plus arbitrary options.  these options will
        # be passed to the frame constructor.
        self.frameklass = frameklass
        self.args = args
        self.kwargs = kwargs

        # when set, the app uses the stdout/stderr window; off by default
        use_stdout_window = 0
        if kwargs.has_key('use_stdout_window'):
            use_stdout_window = kwargs['use_stdout_window']
            del kwargs['use_stdout_window']
        wx.App.__init__(self, use_stdout_window)

    def OnInit(self):
        self.mainframe = self.frameklass(*self.args, **self.kwargs)
        if hasattr(self.mainframe.__class__, "__ExceptHook__"):
            sys.excepthook = self.mainframe.__ExceptHook__
        self.mainframe.Show(True)
        self.SetTopWindow(self.mainframe)
        return True

    def Run(self):
        self.MainLoop()
