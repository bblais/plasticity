import wx
from wx.lib.wordwrap import wordwrap

def AboutBox(parent,info=None,
            name='',version='',copyright='',description='',url='',
            webtitle='',developers=[],license=''):
    
            
    if not info:
        
        info={}
        info['name']=name
        info['version']=version
        info['copyright']=copyright
        info['description']=description
        info['url']=url
        info['webtitle']=webtitle
        info['developers']=developers
        info['license']=license
        
        
        
    ainfo = wx.AboutDialogInfo()
    ainfo.Name = info['name']
    ainfo.Version = info['version']
    ainfo.Copyright = info['copyright']
    
    if '(C)' not in ainfo.Copyright:
        ainfo.Copyright='(C) '+info.Copyright
        
    ainfo.Description = wordwrap(info['description'],
                            350, wx.ClientDC(parent))
    ainfo.WebSite = (info['url'],info['webtitle'])
    ainfo.Developers = info['developers']

    ainfo.License = wordwrap(info['license'], 500, wx.ClientDC(parent))

    # Then we call wx.AboutBox giving it that info object
        
    

    wx.AboutBox(ainfo)

