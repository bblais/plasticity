import wx

class ImagePanel(wx.Panel):

    def __init__(self,parent,id,size=(200,200),image=None,pos=(0,0)):
    
        wx.Panel.__init__(self,parent, id,size=size,pos=pos)
       
        self.image=image
        
        self.bitmap=wx.StaticBitmap(self, -1, image.ConvertToBitmap(),
                                    style=wx.TAB_TRAVERSAL|wx.SIMPLE_BORDER)
        self.update()

    def SetImage(self,image):
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

        
