# tools.py
# Miscellaneous utility functions.

import os
import warnings

def asstring(x):
    """ Ensure that x is a string, i.e. if it's not of the str or unicode
        types, convert it with str.  Otherwise, leave it unchanged. """
    if not (isinstance(x, str) or isinstance(x, unicode)):
        x = str(x)
    return x

def opj(path):
    """Convert paths to the platform-specific separator"""
    str = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        str = '/' + str
    return str

class CheckParentWarning(Warning):
    pass

def parent_warning(obj, container):
    s = "obj %r has parent %r, but is added to container %r" % (
        obj, obj.GetParent(), container)
    warnings.warn(s, CheckParentWarning)

