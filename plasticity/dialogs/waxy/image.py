# image.py

import wx
import waxyobject

_handlers = {}

def AddImageHandler(type):
    d = {
        "bmp": wx.BMPHandler,
        "png": wx.PNGHandler,
        "jpg": wx.JPEGHandler,
        "gif": wx.GIFHandler,
        "pcx": wx.PCXHandler,
        "pnm": wx.PNMHandler,
        "tiff": wx.TIFFHandler,
        #"iff": wx.IFFHandler,
        #"xpm": wx.XPMHandler,
        "ico": wx.ICOHandler,
        "cur": wx.CURHandler,
        "ani": wx.ANIHandler,
    }
    key = type.lower()
    handler = d[key]
    wx.Image_AddHandler(handler())
    _handlers[key] = 1

def AddAllImageHandlers():
    wx.InitAllImageHandlers()

class Image(wx.Image, waxyobject.WaxyObject):

    def __init__(self, filename, type=None, autoinstall=False):
        lfilename = filename.lower()
        t = 0

        # if type isn't set, try to grok it from the filename.
        if not type:
            if lfilename.endswith(".bmp"):
                type = 'bmp'
            elif lfilename.endswith(".gif"):
                type = 'gif'
            elif lfilename.endswith(".png"):
                type = 'png'
            elif lfilename.endswith(".jpg") or lfilename.endswith(".jpeg"):
                type = 'jpg'
            elif lfilename.endswith(".pcx"):
                type = 'pcx'
            elif lfilename.endswith(".ico"):
                type = 'ico'

        t = {
            "bmp": wx.BITMAP_TYPE_BMP,
            "gif": wx.BITMAP_TYPE_GIF,
            "png": wx.BITMAP_TYPE_PNG,
            "jpg": wx.BITMAP_TYPE_JPEG,
            "jpeg": wx.BITMAP_TYPE_JPEG,
            "pcx": wx.BITMAP_TYPE_PCX,
            "ico": wx.BITMAP_TYPE_ICO,
        }.get(type.lower(), 0)

        if not t:
            raise ValueError, "Could not determine bitmap type of '%s'" % (
                  filename,)

        # if autoinstall is true, install handler on demand
        if autoinstall:
            if not _handlers.has_key(type):
                AddImageHandler(type)

        wx.Image.__init__(self, filename, t)


def ImageAsBitmap(filename, *args, **kwargs):
    return Image(filename, *args, **kwargs).ConvertToBitmap()

class ImagePanel(wx.Panel, waxyobject.WaxyObject):

    def __init__(self,parent,image,size=(200,200),pos=(0,0)):
    
        wx.Panel.__init__(self,parent, size=size,pos=pos)
       
        if isinstance(image,str):
            self.image=Image(image)
        else:
            self.image=image
        
        self.bitmap=wx.StaticBitmap(self, -1, self.image.ConvertToBitmap(),
                                    style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.update()

    def SetImage(self,image):
        
        if isinstance(image,str):
            image=Image(image)
            
        self.image=image
        self.update()

    def update(self):
    
        size=self.GetSizeTuple()
        
        imsize=(self.image.GetWidth(),self.image.GetHeight())
        
        if (float(imsize[0])/float(size[0]))>(float(imsize[1])/float(size[1])):
            scale=(float(imsize[0])/float(size[0]))
        else:
            scale=(float(imsize[1])/float(size[1]))
            
        newsize=(int(imsize[0]/scale),int(imsize[1]/scale))
        newpos=( (size[0]-newsize[0])/2, (size[1]-newsize[1])/2)
        self.bitmap.SetBitmap(self.image.Rescale(newsize[0],newsize[1]).ConvertToBitmap())
        self.bitmap.SetPosition(newpos);        

