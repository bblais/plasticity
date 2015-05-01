DEBUG = 0   # set to 1 to enable debugging messages

from wx import BeginBusyCursor, CallAfter, EndBusyCursor, GetActiveWindow, \
                GetApp, Platform, SafeYield, WakeUpIdle, Yield, YieldIfNeeded



if False:
    required = (2, 8, 0, 0) # minimum wxPython version
    required_str = ".".join(map(str, required))
    
    # if a multiversion wxPython is installed, attempt to get a required version
    try:
        # for wxversion, we only take the first two numbers
        import wxversion
        wxversion_req = ".".join(map(str, required[:2]))
        try:
            wxversion.ensureMinimal(wxversion_req)
        except wxversion.VersionError, e:
            # it should also be possible to import wax after wxPython is imported.
            # this VersionError prevents this, so we work around it.
            if e.args[0].find("must be called before wxPython is imported") < 0:
                raise
    except ImportError: # will fail if it's not a multiversion installation
        pass
    
    import wx
    
    assert wx.VERSION >= required, \
           "This version of Wax requires wxPython %s or later" % (required_str,)
    
    DEBUG = 0   # set to 1 to enable debugging messages
    
    from wx import BeginBusyCursor, CallAfter, EndBusyCursor, GetActiveWindow, \
                   GetApp, Platform, SafeYield, WakeUpIdle, Yield, YieldIfNeeded
    
