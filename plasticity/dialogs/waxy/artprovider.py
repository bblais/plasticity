# artprovider.py

import wx, os
import string
import cStringIO

ARTCLIENTS = [ "ART_TOOLBAR",
               "ART_MENU",
               "ART_FRAME_ICON",
               "ART_CMN_DIALOG",
               "ART_HELP_BROWSER",
               "ART_MESSAGE_BOX",
               "ART_OTHER",
               ]

ARTIDS = [ "ART_ADD_BOOKMARK",
           "ART_DEL_BOOKMARK",
           "ART_HELP_SIDE_PANEL",
           "ART_HELP_SETTINGS",
           "ART_HELP_BOOK",
           "ART_HELP_FOLDER",
           "ART_HELP_PAGE",
           "ART_GO_BACK",
           "ART_GO_FORWARD",
           "ART_GO_UP",
           "ART_GO_DOWN",
           "ART_GO_TO_PARENT",
           "ART_GO_HOME",
           "ART_FILE_OPEN",
           "ART_PRINT",
           "ART_HELP",
           "ART_TIP",
           "ART_REPORT_VIEW",
           "ART_LIST_VIEW",
           "ART_NEW_DIR",
           "ART_FOLDER",
           "ART_GO_DIR_UP",
           "ART_EXECUTABLE_FILE",
           "ART_NORMAL_FILE",
           "ART_TICK_MARK",
           "ART_CROSS_MARK",
           "ART_ERROR",
           "ART_QUESTION",
           "ART_WARNING",
           "ART_INFORMATION",
           ]

class ArtProvider(object):
    def __init__(self, size=wx.DefaultSize):
        self.custom = {}
        self.clients = []
        for client in ARTCLIENTS:
            self.clients.append(client[4:].lower())
        self.images = []
        for image in ARTIDS:
            self.images.append(image[4:].lower())
        self.size = size
        self._usecustom = False

    def _SetUseCustom(self, value):
        if self._usecustom and not value:
            wx.ArtProvider_PopProvider()
        elif value and not self._usecustom:
            wx.ArtProvider_PushProvider(ArtPushProvider(self))
        self._usecustom = value

    def _GetUseCustom(self):
        return self.__usecustom

    UseCustom = property(_GetUseCustom, _SetUseCustom, doc="Custom art enable")

    def _GetWxArtIds(self, name, client):
        imageid = "ART_" + name.upper()
        clientid = "ART_" + client.upper()
        wx_image = getattr(wx, imageid, name)
        wx_client = getattr(wx, clientid, client)
        return wx_image, wx_client

    def GetBitmap(self, image, client='other', size=None):
        wx_image, wx_client = self._GetWxArtIds(image, client)
        if size == None:
            size = self.size
        return wx.ArtProvider_GetBitmap(wx_image, wx_client, size)

    def GetIcon(self, name, client='other', size=None):
        wx_image, wx_client = self._GetWxArtIds(name, client)
        if size == None:
            size = self.size
        return wx.ArtProvider_GetIcon(wx_image, wx_client, size)

    def RegisterImage(self, image, name, client='other', size=None):
        wx_image, wx_client = self._GetWxArtIds(name, client)
        if size == None:
            size = self.size
        keyword = string.join([wx_client,"::", wx_image, "::", str(size[0]),":", str(size[1])],'')
        if size != (-1,-1):
            image.Rescale(size[0], size[1])
        self.custom[keyword] = wx.BitmapFromImage(image)
        if wx_client not in self.clients:
            if not wx_client.startswith('wxART'):
                self.clients.append(wx_client)
        if wx_image not in self.images:
            if not wx_image.startswith('wxART'):
                self.images.append(wx_image)

    def RegisterFromFile(self, filename, name, client='other', size=None):
        image = wx.Image(opj(filename), wx.BITMAP_TYPE_ANY)
        self.RegisterImage(image, name, client, size)

    def RegisterFromData(self, stream, name, client='other', size=None):
        image = wx.ImageFromStream(stream)
        self.RegisterImage(image, name, client, size)

class ArtPushProvider(wx.ArtProvider):
    # custom class for push_provider
    def __init__(self, waxArtProvider):
        wx.ArtProvider.__init__(self)
        self.__AP = waxArtProvider

    def CreateBitmap(self, artid, client, size):
        keyword = string.join([client,"::", artid, "::", str(size[0]),":", str(size[1])],'')
        bmp = wx.NullBitmap
        if self.__AP.custom.has_key(keyword):
            bmp = self.__AP.custom[keyword]
        return bmp

