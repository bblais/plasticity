# bitmap.py

import wx
import waxyobject
import image
import cStringIO

# XXX not sure what to do with this
class Bitmap(wx.StaticBitmap, waxyobject.WaxyObject):

    def __init__(self, parent, bitmap):
        if isinstance(bitmap, str) or isinstance(bitmap, unicode):
            bitmap = BitmapFromFile(bitmap)
        wx.StaticBitmap.__init__(self, parent, wx.NewId(), bitmap)
        # XXX supposedly you can load this from file too?

#
# use these functions for convenience...
# unfortunately, they return wxBitmaps, not Bitmaps

def BitmapFromData(data):
    stream = cStringIO.StringIO(data)
    z = wx.ImageFromStream(stream)
    return wx.BitmapFromImage(z)

def BitmapFromFile(filename):
    data = open(filename, 'rb').read()
    return BitmapFromData(data)

