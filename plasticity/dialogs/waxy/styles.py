# styles.py

import wx


NORMAL    = 0
EXCLUDE   = 1
DICT      = 2
DICTSTART = 3
REVERSE   = 32


def styledict(name, dict, kwargs, default=0):
    flags = 0
    if kwargs.has_key(name):
        value = kwargs[name]
        try:
            value = value.lower()
        except AttributeError:
            pass
        flags |= dict.get(value, default)
        del kwargs[name]
    return flags

def styledictstart(name, dict, kwargs, default=0):
    """ Like styledict, but matches the first letter(s) rather than the
        complete value.  For example, if "lower" is the only key in the dict
        starting with "l", then by passing the value "l" we match "lower".
        Used e.g. in _button_align.
    """
    flags = 0
    if kwargs.has_key(name):
        value = kwargs[name].lower()
        # note that we traverse the dict pair by pair, so ambiguous matches
        # *are* possible
        for key, flag in dict.items():
            if key.startswith(value):
                flags |= flag
                break
        else:
            flags |= default
        del kwargs[name]
    return flags

def stylebool(name, flag, kwargs, reverse=0):
    """ If <name> is in kwargs and is true, then return <flag>.
        If <reverse> is set, then the condition needs to be false in order
        for the flag to be returned.
        (E.g. stylebool('lines', wx.BLAH_NOLINES, kwargs, reverse=1)
        will return wx.BLAH_NOLINES if lines==0, not if lines==1.)
    """
    flags = 0
    if kwargs.has_key(name):
        value = kwargs[name]
        if reverse:
            value = not value
        if value:
            flags |= flag
        del kwargs[name]
    return flags

def styleboolexclude(name, flag, kwargs, reverse=0):
    flags = 0
    if kwargs.has_key(name):
        value = kwargs[name]
        if reverse:
            value = not value
        if value:
            flags |= flag
        del kwargs[name]
    return flags

def stylebooleither(name, flagtrue, flagfalse, kwargs):
    flags = 0
    if kwargs.has_key(name):
        value = kwargs[name]
        if value:
            flags |= flagtrue
        else:
            flags |= flagfalse
        del kwargs[name]
    return flags

# not sure if this can be used...
def stylefunc(name, func, kwargs):
    if kwargs.has_key(name):
        value = kwargs[name]
        func(value)
        del kwargs[value]
    return 0

#
#
#
def dostyle(styledict, kwargs):
    """ Set styles for a given control, using a "style dict".  Return the 
        eventual flag value.  Mostly for internal use. """
    flags = 0
    for k, (style, type) in styledict.items():
        #style, type = styledict[k]
        # First check for reversing
        reverse = 0
        if (type & REVERSE) == REVERSE:
            reverse = 1
        # Get everything but the `reverse` bits
        type = type & (reverse - 1)
        # Now see what we're dealing with
        if type == NORMAL:
            flags |= stylebool(k, style, kwargs, reverse=reverse)
        elif type == DICT:
            flags |= styledict(k, style, kwargs)
        elif type == DICTSTART:
            flags |= styledictstart(k, style, kwargs)
        elif type == EXCLUDE:
            flags &= ~styleboolexclude(k, style, kwargs, reverse=reverse)

    return flags
#
# the following functions do not handle flags

def properties(obj, kwargs):
    """ Called by constructors to set properties from a dict.  Must be called
        *after* the parent's constructor (unlike most of the other styles
        functions). """
    if kwargs.has_key('properties'):
        d = kwargs['properties']
        for key, value in d.items():
            setattr(obj, key, value)  # attempt to set property
        del kwargs['properties']

    # attempt to set the remaining attributes as properties (this will raise
    # an error if an invalid property name is specified).
    obj.SetProperties(**kwargs)

    # XXX could be a method in WaxyObject... if it doesn't already exist?


#
# window styles

_window_border = {
    "simple": wx.SIMPLE_BORDER,
    "double": wx.DOUBLE_BORDER,
    "sunken": wx.SUNKEN_BORDER,
    "raised": wx.RAISED_BORDER,
    "static": wx.STATIC_BORDER,
    "no": wx.NO_BORDER,
    "none": wx.NO_BORDER,
}

def window(kwargs):
    """ Styles applicable to any wx.Window descendant. """
    flags = 0
    flags |= styledict('border', _window_border, kwargs)
    flags |= stylebool('transparent', wx.TRANSPARENT_WINDOW, kwargs)
    flags |= stylebool('tab_traversal', wx.TAB_TRAVERSAL, kwargs)
    flags |= stylebool('wants_chars', wx.WANTS_CHARS, kwargs)

    return flags

