# waxyobject.py

import wx
import core
import colordb
import events
import mousepointer
import styles

class MetaWaxyObject(type):

##    def inject_SetFont(cls):
##        if hasattr(cls, "SetFont"):
##            real_SetFont = getattr(cls, "SetFont")
##            def SetFont(self, obj):
##                if isinstance(obj, tuple):
##                    import font
##                    obj = font.Font(*obj)
##                real_SetFont(self, obj)
##            SetFont.__doc__ = real_SetFont.__doc__
##            setattr(cls, "SetFont", SetFont)
##            if core.DEBUG:
##                print "%s: SetFont replaced" % (cls,)
##
##    def inject_GetFont(cls):
##        if hasattr(cls, "GetFont"):
##            real_GetFont = getattr(cls, "GetFont")
##            import font
##            def GetFont(self):
##                wxfont = real_GetFont(self)
##                wxfont.__class__ = font.Font
##                return wxfont
##            GetFont.__doc__ = real_GetFont.__doc__
##            setattr(cls, "GetFont", GetFont)
##            if core.DEBUG:
##                print "%s: GetFont replaced" % (cls,)

    def inject_SetCursor(cls):
        if hasattr(cls, "SetCursor"):
            real_SetCursor = getattr(cls, "SetCursor")
            def SetCursor(self, x):
                if isinstance(x, basestring):
                    c = mousepointer.MousePointers.Get(x)
                    real_SetCursor(self, c)
                else:
                    real_SetCursor(self, x)
            SetCursor.__doc__ = real_SetCursor.__doc__
            setattr(cls, "SetCursor", SetCursor)
            if core.DEBUG:
                print "%s: SetCursor replaced" % (cls,)

    def inject_SetWindowStyle(cls):
        if hasattr(cls, "SetWindowStyle"):
            real_SetWindowStyle = getattr(cls, "SetWindowStyle")
            def SetWindowStyle(self, __default__=0, **kwargs):
                """ Wax-style SetWindowStyle that supports the old way of
                    setting styles (using an integer flag value), and/or
                    named keywords, depending on the class's _params method.
                """
                flags = __default__
                flags |= self._params(kwargs)
                if isinstance(self, wx.Window):
                    flags |= styles.window(kwargs)
                real_SetWindowStyle(self, flags)
            setattr(cls, "SetWindowStyle", SetWindowStyle)
            if core.DEBUG:
                print "%s: SetWindowStyle replaced" % (cls,)

    def inject_ColorMethods(cls):
        if hasattr(cls, "SetBackgroundColour"):
            real_SetBackgroundColour = getattr(cls, "SetBackgroundColour")
            real_SetForegroundColour = getattr(cls, "SetForegroundColour")

            def SetForegroundColour(self, color):
                color = colordb.convert_color(color)
                real_SetForegroundColour(self, color)
            SetForegroundColour.__doc__ = real_SetForegroundColour.__doc__
            setattr(cls, "SetForegroundColour", SetForegroundColour)

            def SetBackgroundColour(self, color):
                color = colordb.convert_color(color)
                real_SetBackgroundColour(self, color)
            SetBackgroundColour.__doc__ = real_SetBackgroundColour.__doc__
            setattr(cls, "SetBackgroundColour", SetBackgroundColour)

            # make aliases for "Color"
            setattr(cls, "SetBackgroundColor", cls.SetBackgroundColour)
            setattr(cls, "SetForegroundColor", cls.SetForegroundColour)
            setattr(cls, "GetBackgroundColor", cls.GetBackgroundColour)
            setattr(cls, "GetForegroundColor", cls.GetForegroundColour)

            if core.DEBUG:
                print "%s: SetForegroundColour/SetBackgroundColour replaced" % (cls,)

    def __init__(cls, name, bases, dict):
#        cls.inject_SetFont()
#        cls.inject_GetFont()
        cls.inject_SetCursor()
        cls.inject_ColorMethods()
        cls.inject_SetWindowStyle()


class WaxyObject:
    """ Mixin class for Wax controls.
        Stick attributes and methods here that every Wax control should have.
    """
    __metaclass__ = MetaWaxyObject
    # yes, I don't like metaclasses, but they're actually useful here :-)

    __events__ = {}
    __styles__ = {}

##    def SetDefaultFont(self):
##        if hasattr(self, 'SetFont'):
##            self.SetFont(waxconfig.WaxConfig.default_font)

    def SetSizeX(self, ix):
        x, y = self.GetSize()
        self.SetSize((ix, y))

    def SetSizeY(self, iy):
        x, y = self.GetSize()
        self.SetSize((x, iy))
        
    def GetSizeX(self):
        return self.GetSize()[0]
        
    def GetSizeY(self):
        return self.GetSize()[1]

    def BindEvents(self):
        items = []
        if hasattr(self, "__events__"):
            items = getattr(self, "__events__").items()
        items.extend(events.events.items())
        for name, wxevent in items:
            if hasattr(self, "On" + name):
                f = getattr(self, "On" + name)
                self.Bind(wxevent, f)
                if core.DEBUG:
                    print "Binding %s to %s" % (name, f)

    def GetAllChildren(self):
        """ Return a generator returning all children, grandchildren, etc,
            of the given widget.  The widgets are traversed depth-first.
        """
        if hasattr(self, 'GetChildren'):
            for child in self.GetChildren():
                yield child
                for grandchild in child.GetAllChildren():
                    yield grandchild

    #
    # pseudo-properties

    def __getattr__(self, name):
        if hasattr(self.__class__, "Get" + name):
            # use self.__class__ rather than self to avoid recursion
            f = getattr(self, "Get" + name)
            return f()
        else:
            raise AttributeError, name

    def __setattr__(self, name, value):
        if hasattr(self, "Set" + name):
            f = getattr(self, "Set" + name)
            return f(value)
        elif name.startswith("On"):
            shortname = name[2:]
            if self.__events__.has_key(shortname):
                wxevent = self.__events__[shortname]
            elif events.events.has_key(shortname):
                wxevent = events.events[shortname]
            else:
                wxevent = None
            self.__dict__[name] = value
            if wxevent:
                self.Bind(wxevent, value)
                if core.DEBUG:
                    print "Binding %s to %s" % (name, value)
        else:
            self.__dict__[name] = value

    def SetAttributes(self, **kwargs):
        """ Set a number of attributes at once.  E.g.
            widget.SetAttributes(Font=MYFONT, Size=(100,200))
        """
        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

    def SetProperties(self, **kwargs):
        """ As SetAttributes, but raises an error if an unknown property name
            is specified. """
        for (key, value) in kwargs.items():
            f = getattr(self, "Set" + key, None)
            if f:
                f(value)
            else:
                raise AttributeError, "Unknown property: %s" % (key,)

    def _params(self, kwargs, thesestyles={}):
        # default method for those controls that don't have a _params()
        if thesestyles:
            return styles.dostyle(thesestyles, kwargs)
        else:
            return styles.dostyle(self.__styles__, kwargs)

    def HasStyle(self, style, substyle=None):
        """ Returns whether or not a style is set for this object. """
        try:
            sval = self.__styles__[style][0]
            if isinstance(sval, dict):
                # The style returned is a complex style so...
                if substyle:
                    # ...checking for a specific substyle, return if it's set
                    subval = sval[substyle]
                    ws = self.GetWindowStyle()
                    # If we're dealing with a zero based style, things
                    #  get a bit trickier
                    if subval == 0:
                        for k in sval:
                            temp = sval[k]
                            if k != substyle and (ws & temp) == temp:
                                return False
                    return (ws & subval) == subval
                else:
                    # ...not checking for specific, so see if either is set and
                    #  return the key value associated with what is set
                    mystyle = self.GetWindowStyle()
                    for k in sval:
                        v = sval[k]
                        if (mystyle & v) == v:
                            return k
                    return False
            else:
                # Style is not complex, return if it is set or not
                return (self.GetWindowStyle() & sval) == sval
        except:
            return False

    def GetStyleDict(self):
        """ Returns a dictionary with style info for this object. """
        ret = {}
        for k in self.__styles__:
            ret[k] = self.HasStyle(k)
        return ret
