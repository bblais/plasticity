# mousepointer.py

# TODO:
# - remove code duplication in LoadImage/LoadStream

import wx
import colordb
import os
import sys
import utils

POINTERS = {
    "arrow" : wx.CURSOR_ARROW,
    "arrowright" : wx.CURSOR_RIGHT_ARROW,
    "bullseye" : wx.CURSOR_BULLSEYE,
    "char" : wx.CURSOR_CHAR,
    "cross" : wx.CURSOR_CROSS,
    "hand" : wx.CURSOR_HAND,
    "ibeam" : wx.CURSOR_IBEAM,
    "buttonleft" : wx.CURSOR_LEFT_BUTTON,
    "magnifier" : wx.CURSOR_MAGNIFIER,
    "buttonmiddle" : wx.CURSOR_MIDDLE_BUTTON,
    "noentry" : wx.CURSOR_NO_ENTRY,
    "paintbrush" : wx.CURSOR_PAINT_BRUSH,
    "pencil" : wx.CURSOR_PENCIL,
    "pointleft" : wx.CURSOR_POINT_LEFT,
    "pointright" : wx.CURSOR_POINT_RIGHT,
    "arrowquestion" : wx.CURSOR_QUESTION_ARROW,
    "buttonright" : wx.CURSOR_RIGHT_BUTTON,
    "sizenesw" : wx.CURSOR_SIZENESW,
    "sizens" : wx.CURSOR_SIZENS,
    "sizenwse" : wx.CURSOR_SIZENWSE,
    "sizewe" : wx.CURSOR_SIZEWE,
    "sizing" : wx.CURSOR_SIZING,
    "spraycan" : wx.CURSOR_SPRAYCAN,
    "wait" : wx.CURSOR_WAIT,
    "watch" : wx.CURSOR_WATCH,
    "blank" : wx.CURSOR_BLANK,
    "default" : wx.CURSOR_DEFAULT,
    "arrowcopy" : wx.CURSOR_COPY_ARROW,
    "arrowwait" : wx.CURSOR_ARROWWAIT,
    }

class MousePointerRegistry:
    def __init__(self):
        self.custom = {}
    def Get(self, name):
        if POINTERS.has_key(name):
            return wx.StockCursor(POINTERS[name]) # return a cursor
        elif self.custom.has_key(name):
            return self.custom[name] # return an image-as-cursor
        else:
            raise KeyError, "Unknown pointer name: %s" % (name,)
    def Set(self, name, value):
        self.custom[name] = value
    Register = Set
    def GetBuiltinNames(self):
        return POINTERS.keys()
    def GetCustomNames(self):
        return self.custom.keys()
    def GetNames(self):
        return self.GetBuiltinNames() + self.GetCustomNames()

    def _RegisterImage(self, name, image, maskcolor='white', hotx=None, hoty=None):
        """ Register a wx.Image as a cursor. """
        if sys.platform =='win32':
            #cursors fixed size 32,32
            xratio = image.GetWidth() / 32
            yratio = image.GetHeight() / 32
        else:
            xratio = yratio = 1
        if not image.HasMask():
            c = colordb.convert_color(maskcolor)
            image.SetMaskColour(c[0], c[1], c[2])
        if not hotx:
            hotx = image.GetWidth() / 2
        hotx = hotx / xratio
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, hotx)
        if not hoty:
            hoty = image.GetHeight() / 2
        hoty = hoty / yratio
        image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, hoty)
        self.custom[name] = wx.CursorFromImage(image)

    def RegisterImage(self, name, filename, maskcolor='white', hotx=None, hoty=None):
        i = wx.Image(utils.opj(filename), wx.BITMAP_TYPE_ANY)
        self._RegisterImage(name, i, maskcolor, hotx, hoty)

    def RegisterStream(self, name, stream, maskcolor='white', hotx=None, hoty=None):
        i = wx.ImageFromStream(stream)
        self._RegisterImage(name, i, maskcolor, hotx, hoty)


# global registry
MousePointers = MousePointerRegistry()
