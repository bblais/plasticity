from waxy import *
from mywaxy import *

import math
from utils import *

def FileInfo(fname):
    
    var=[]
    try:
        var=hdf5_load_images(fname)
    except IOError:
        infostr="File %s not found" % fname
        
    if var:
        mn=min([im.min() for im in var['im']])*var['im_scale_shift'][0]+var['im_scale_shift'][1]
        mx=max([im.max() for im in var['im']])*var['im_scale_shift'][0]+var['im_scale_shift'][1]
        infostr="""Filename: %s\nSize: %dx%dx%d\nMin: %.4e\nMax: %.4e""" % (fname,var['im'][0].shape[0],var['im'][0].shape[1],len(var['im']),mn,mx)

    dlg=MessageDialog(None,
                  text=infostr,
                  title="File Information")
    result=dlg.ShowModal()
    dlg.Destroy()
    
    
class ChannelPanel(Panel):
    
    def __init__(self,parent,pattern,noise):
        Panel.__init__(self,parent,direction='horizontal')
        
        
        self.pattern=pattern
        self.noise=noise
        self.line=[]
        
        var=[]
        
        
        self.fname=pattern['filename']
        
        if not self.fname.startswith('/'):
            basename=os.path.dirname(__file__)
            self.fname=basename+"/../"+self.fname
        
        if self.fname:
            try:
                var=hdf5_load_images(self.fname)
            except IOError:
                var=None
                
    
        if not var:
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
            self.fname=''
        elif pattern['type']==1: # data
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
        else:        
            im=array2image(var['im'][0],rescale=True)

        
        panel2=Panel(self,direction='vertical')
        
        self.image_panel=ImagePanel(panel2,im,size=(200,200))    
        panel2.AddComponent(self.image_panel,expand='h')

        b=Button(panel2,'File Information',self.Info)
        panel2.AddComponent(b,expand='h')
        
        panel2.Pack()
        
        self.AddComponent(panel2,border=2)

        panel2=Panel(self,direction='vertical')

        
        choices=['None','Data Vectors','Image Patches']
        self.type_combobox=DropDownBox(panel2,choices)
        self.type_combobox.SetSelection(self.pattern['type'])
        self.type_combobox.OnSelect=self.Pattern_Type
        panel2.AddComponent(self.type_combobox,expand='h')
        
        
        panel3=Panel(panel2,direction='horizontal')
        
        self.fname_textbox=TextBox(panel3,self.fname,multiline=0,size=(180,-1))
        self.fname_textbox.OnLoseFocus=self.UpdateBitmap
        panel3.AddComponent(self.fname_textbox,expand='h')
        self.fname_browse_button=Button(panel3,"Browse",self.Browse)
        panel3.AddComponent(self.fname_browse_button)
        panel3.Pack()
        panel2.AddComponent(panel3)

        
        
        panel3=Panel(panel2,direction='horizontal')
        
        n=pattern['num_inputs']
        if pattern['type']==2:  # images
            n_str='%d*%d' % (math.sqrt(n),math.sqrt(n))
        else:
            n_str=str(n)
            
        self.pattern_num_inputs_textbox=TextBox(panel3,n_str,multiline=0,size=(180,-1))
        panel3.AddComponent(Label(panel3,"Number of Inputs: "))
        panel3.AddComponent(self.pattern_num_inputs_textbox,expand='h')
        panel3.Pack()
        panel2.AddComponent(panel3)
        
        panel3=Panel(panel2,direction='horizontal')
        self.pattern_scale_textbox=TextBox(panel3,str(pattern['scale']),
                                            multiline=0,size=(180,-1))
        panel3.AddComponent(Label(panel3,"Scale: "))
        panel3.AddComponent(self.pattern_scale_textbox,expand='h')
        panel3.Pack()
        panel2.AddComponent(panel3)
        

        
        self.pattern_sequential=CheckBox(panel2,"Use Sequential Images/Vectors")
        panel2.AddComponent(self.pattern_sequential)
        self.pattern_sequential.Enable(False)

        self.pattern_mask=CheckBox(panel2,"Use Circle Mask")
        if pattern['masktype']=='circle':
            self.pattern_mask.SetValue(1)
        else:
            self.pattern_mask.SetValue(0)

        panel2.AddComponent(self.pattern_mask)
        panel2.Pack()
        self.AddComponent(panel2,border=10)

        # add line
        line = Line(self, size=(-1,20), direction='vertical')
        self.AddComponent(line, align='center', expand='v', border=15)
        

        
        t=noise['type']
        n=noise
        
        if t==0: # none
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
        elif t==1: # uniform
            im=array2image(numpy.random.rand(200,200),rescale=True)
        elif t==2: # gaussian
            im=array2image(numpy.random.randn(200,200),rescale=True)
        elif t==3: # laplace
            im=array2image(numpy.random.laplace(size=(200,200)),rescale=True)
        elif t==4: # proportional
            im=array2image(numpy.random.randn(200,200),rescale=True)
        else:
            raise ValueError
        
            
        panel2=Panel(self,direction='vertical')

        self.noise_image_panel=ImagePanel(panel2,im,size=(200,200))
        panel2.AddComponent(self.noise_image_panel)
        
        b=Button(panel2,'Info')
        panel2.AddComponent(b,expand='h')
        
        panel2.Pack()
        self.AddComponent(panel2)

        
        panel2=Panel(self,direction='vertical')

        
        choices=['None','Uniform','Gaussian','Laplace','Proportional']
        self.noise_type_combobox=DropDownBox(panel2,choices,size=(180,-1))
        self.noise_type_combobox.SetStringSelection(choices[self.noise['type']])
        self.noise_type_combobox.OnSelect=self.Noise_Type
        panel2.AddComponent(self.noise_type_combobox,expand='h')
        
        
        panel3=Panel(panel2,direction='horizontal')
        self.noise_mean_textbox=TextBox(panel3,str(self.noise['mean']),multiline=0,size=(180,-1))
        panel3.AddComponent(Label(panel3,"Mean: "))
        panel3.AddComponent(self.noise_mean_textbox,expand='h')
        panel3.Pack()
        panel2.AddComponent(panel3)

        panel3=Panel(panel2,direction='horizontal')
        self.noise_std_textbox=TextBox(panel3,str(self.noise['std']),multiline=0,size=(180,-1))
        panel3.AddComponent(Label(panel3,"Std: "))
        panel3.AddComponent(self.noise_std_textbox,expand='h')

        
        
        panel3.Pack()
        panel2.AddComponent(panel3)

        panel2.Pack()
        self.AddComponent(panel2,border=10)
        
        
        self.Pack()
        
        self.Pattern_Type()
        self.Noise_Type()
        
        
    def Pattern_Type(self,event=None):
        if event:
            self.pattern['type']=event.GetSelection()
        else:
            self.pattern['type']=self.type_combobox.GetSelection()
            
        
        if self.pattern['type']==0:
            self.fname_textbox.Enable(False)
            self.fname_browse_button.Enable(False)
        else:
            self.fname_textbox.Enable(True)
            self.fname_browse_button.Enable(True)
            
        self.UpdateBitmap()
        
    def Noise_Type(self,event=None):
        if event:
            self.noise['type']=event.GetSelection()
        else:
            self.noise['type']=self.noise_type_combobox.GetSelection()
        
        if self.noise['type']==0:
            self.noise_mean_textbox.Enable(False)
            self.noise_std_textbox.Enable(False)
        else:
            self.noise_mean_textbox.Enable(True)
            self.noise_std_textbox.Enable(True)
            
        self.UpdateBitmap()
        
    def UpdateValues(self,event=None):
        
        self.noise['type']=self.noise_type_combobox.GetSelection()
        self.pattern['type']=self.type_combobox.GetSelection()
        
            
        self.pattern['filename']=self.fname_textbox.GetValue()
        self.pattern['var']=[]

        
        n_str=self.pattern_num_inputs_textbox.GetValue()
        try:
            n=eval("int("+n_str+")")
        except (SyntaxError,NameError):
            Error("Syntax error in num inputs.  Ignoring.")
            n=None
                
        if n:
            self.pattern['num_inputs']=n
        
        val=float(self.pattern_scale_textbox.GetValue())
        self.pattern['scale']=val
        
        val=float(self.noise_mean_textbox.GetValue())
        self.noise['mean']=val
        
        val=float(self.noise_std_textbox.GetValue())
        self.noise['std']=val

        if self.pattern_mask.IsChecked():
            self.pattern['masktype']='circle'
        else:
            self.pattern['masktype']='none'
            

        self.Pattern_Type()
        self.Noise_Type()

        
    def UpdateBitmap(self,event=None):

        typ=self.type_combobox.GetSelection()
        self.fname=self.fname_textbox.GetValue()
        
        if typ:
            var=[]
            if self.fname:
                try:
                    var=hdf5_load_images(self.fname)
                except IOError:
                    var=None
        else:
            var=None
    
        if not var:
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
            self.fname=None
        elif self.pattern['type']==1: # data
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
        else:
            im=array2image(var['im'][0],rescale=True)

        self.image_panel.SetImage(im)
        
        t=self.noise['type']
        n=self.noise
        
        if t==0: # none
            im=array2image(numpy.ones((200,200),numpy.uint8)*100)
        elif t==1: # uniform
            im=array2image(numpy.random.rand(200,200),rescale=True)
        elif t==2: # gaussian
            im=array2image(numpy.random.randn(200,200),rescale=True)
        elif t==3: # laplace
            im=array2image(numpy.random.laplace(size=(200,200)),rescale=True)
        elif t==4: # proportional
            im=array2image(numpy.random.randn(200,200),rescale=True)
        else:
            raise ValueError
        
        
        self.noise_image_panel.SetImage(im)
        
    def Browse(self,event):
        dlg = FileDialog(self, "Choose Picture File",default_dir=os.getcwd()+"/hdf5",
                        wildcard='HDF5 Files|*.hdf5|PICS Files|*.pics|DAT Files|*.dat|All Files|*.*')
        result = dlg.ShowModal()
        if result == 'ok':
            self.fname = dlg.GetPaths()[0]
            if self.fname.startswith(os.getcwd()):
                self.fname=self.fname.replace(os.getcwd(),'')
                self.fname=self.fname.strip('/')
            self.fname_textbox.SetValue(self.fname)
            self.UpdateBitmap()
        dlg.Destroy()
        
        
    def Info(self,event):
        FileInfo(self.fname)
        

        
        
class Input_Parameters_Dialog(Dialog):
    
    def __init__(self,parent=None,title="",info=None):
        
        self.info=info
        Dialog.__init__(self,parent,title)
    
    def Nop(self,event):
        pass
    
    def OnClickOKButton(self,event):

        for c in self.channels:
            c.UpdateValues()
        
            
        self.info['pattern_input']=[]
        self.info['noise_input']=[]
        
        for c in self.channels:
            self.info['pattern_input'].append(c.pattern)
            self.info['noise_input'].append(c.noise)
            
        Dialog.OnClickOKButton(self,event)
    
    def AddChannel(self,event):
        
        self.AddChannels(2)
        
    def RemoveChannel(self,event=None):
        
        if (len(self.channels)>1):
            c=self.channels.pop()
            c.line.Destroy()
            c.Destroy()
        
        self.spanel.Repack()
        self.spanel.SetupScrolling()

    def SetNumChannels(self,event=None):
        
        try:
            new_num_channels=event.GetSelection()+1
        except AttributeError:  # an integer sent
            new_num_channels=event 
            
            
        num_channels=len(self.channels)

        if new_num_channels==num_channels:
            return
        
        if new_num_channels==(self.max_channels+1): # custom
            new_num_channels=Input_Integer('Number of Channels',
                            'Input the Number of Channels',default=10,
                            parent=self)
        
        if not new_num_channels:
            return
                            
        extra_channels=new_num_channels-num_channels
        
        if (extra_channels>0):
            self.AddChannels(extra_channels)
        else:
            for i in range(-extra_channels):
                self.RemoveChannel()
        
        
        
    def AddChannels(self,extra_channels):

        num_channels=len(self.channels)
        
        for c in self.channels:
            c.UpdateValues()
            
        for i in range(extra_channels):
            
            p=copy(self.channels[i%num_channels].pattern)
            n=copy(self.channels[i%num_channels].noise)
            
            self.channels.append(ChannelPanel(self.spanel,p,n))
            self.spanel.AddComponent(self.channels[-1],border=10)
    
            # add line
            line = Line(self.spanel, size=(20,-1), direction='horizontal')
            self.spanel.AddComponent(line, align='center', expand='h', border=2)

            self.channels[-1].line=line
            
        self.spanel.Repack()
        self.spanel.SetupScrolling()
        
    def Body(self):
        
        num_channels=len(self.info['pattern_input'])
        panel=Panel(self,direction='vertical')

        self.max_channels=10
        choices=['%d Channels'% i for i in range(1,self.max_channels+1)]
        choices[0]='1 Channel'
        choices.append('Custom')    
        
        self.num_channels_dropdown=DropDownBox(panel,choices)
        self.num_channels_dropdown.OnSelect=self.SetNumChannels
        
        if num_channels<=self.max_channels:
            self.num_channels_dropdown.SetSelection(num_channels-1)
        else:
            self.num_channels_dropdown.SetSelection(self.max_channels)
            
        panel.AddComponent(self.num_channels_dropdown)
        
        choices=['Standard Experiments',
                'Normal Rearing',
                'Monocular Deprivation',
                'Binocular Deprivation',
                'Reverse Occlusion']
                
        self.stdexp=DropDownBox(panel,choices)
        panel.AddComponent(self.stdexp)
        self.stdexp.SetSelection(0)
        self.stdexp.OnSelect=self.SetStdExp
        
        panel.Pack()
        self.AddComponent(panel)
        
        panel=Panel(self,direction='horizontal')
        self.AddHeading(panel,"Pattern")
        self.AddHeading(panel,"Noise")
        panel.Pack()
        self.AddComponent(panel,expand='h',align='c')
        
        self.spanel=ScrollPanel(self,direction='vertical')
        
        self.channels=[]
        for i,p,n in zip(range(num_channels),self.info['pattern_input'],self.info['noise_input']):
            self.channels.append(ChannelPanel(self.spanel,p,n))
            self.spanel.AddComponent(self.channels[-1],border=10)

            # add line
            line = Line(self.spanel, size=(20,-1), direction='horizontal')
            self.spanel.AddComponent(line, align='center', expand='h', border=2)

            self.channels[-1].line=line
            
            if i==1:
                self.spanel.Pack()
                self.spanel.SetupScrolling()
                
            

        self.spanel.Pack()
        self.spanel.SetupScrolling()
        
        self.AddComponent(self.spanel, expand='both', border=3)

    def SetStdExp(self,event):
        
        expt=event.GetSelection()
        
        if expt==0:
            return
        
        fname='hdf5/new_images12_dog.hdf5'
        typ=2
        noise_type=1
        noise_mean=0.0
        noise_std=1.0
        for c in self.channels:
            if c.pattern['filename'] and c.pattern['type']:
                fname=c.pattern['filename']
                typ=c.pattern['type']
                break
                
            if c.noise['type']:
                noise_type=c.noise['type']
                noise_mean=c.noise['mean']
                noise_std=c.noise['std']
                
        
        
        
        if expt==1:  # normal rearing
            
            self.SetNumChannels(2)
            self.channels[0].type_combobox.SetSelection(typ)
            self.channels[1].type_combobox.SetSelection(typ)
            
            self.channels[0].fname_textbox.SetValue(fname)
            self.channels[1].fname_textbox.SetValue(fname)
            
            self.channels[0].pattern_scale_textbox.SetValue('1')
            self.channels[1].pattern_scale_textbox.SetValue('1')

            self.channels[0].noise_type_combobox.SetSelection(0)
            self.channels[1].noise_type_combobox.SetSelection(0)

        if expt==2:  # monocular deprivation
            self.SetNumChannels(2)
            self.channels[0].type_combobox.SetSelection(0)
            
            self.channels[1].type_combobox.SetSelection(typ)
            self.channels[1].fname_textbox.SetValue(fname)
            self.channels[1].pattern_scale_textbox.SetValue('1')

            self.channels[0].noise_type_combobox.SetSelection(noise_type)
            self.channels[0].noise_mean_textbox.SetValue(str(noise_mean))
            self.channels[0].noise_std_textbox.SetValue(str(noise_std))
        
            self.channels[1].noise_type_combobox.SetSelection(0)
        
        if expt==3:  # binocular deprivation
            self.SetNumChannels(2)
            self.channels[0].type_combobox.SetSelection(0)
            self.channels[1].type_combobox.SetSelection(0)

            self.channels[0].noise_type_combobox.SetSelection(noise_type)
            self.channels[0].noise_mean_textbox.SetValue(str(noise_mean))
            self.channels[0].noise_std_textbox.SetValue(str(noise_std))

            self.channels[1].noise_type_combobox.SetSelection(noise_type)
            self.channels[1].noise_mean_textbox.SetValue(str(noise_mean))
            self.channels[1].noise_std_textbox.SetValue(str(noise_std))


        if expt==4:  # reverse occlusion
            self.SetNumChannels(2)
            self.channels[1].type_combobox.SetSelection(1)

            self.channels[0].type_combobox.SetSelection(typ)
            self.channels[0].fname_textbox.SetValue(fname)
            self.channels[0].pattern_scale_textbox.SetValue('1')

            self.channels[1].noise_type_combobox.SetSelection(noise_type)
            self.channels[1].noise_mean_textbox.SetValue(str(noise_mean))
            self.channels[1].noise_std_textbox.SetValue(str(noise_std))

            self.channels[0].noise_type_combobox.SetSelection(0)
        
        
        for c in self.channels:
            c.UpdateValues()
        
    def AddHeading(self,parent,txt):
        
        l=Label(parent,txt,align='c')
        
        f=Font(l.GetFont().GetFaceName(),16,bold=1,underline=1)
        l.SetFont(f)
        
        parent.AddComponent(l,align='c',expand='h')
        
        
        
def set_input_parameters(params,parent=None):
    
    keys=['pattern_input', 
          'noise_input']
    
    
    info=deepcopy(subdict(params,keys))
    
    if not parent:
        app = Application(EmptyFrame)
        
    dlg=Input_Parameters_Dialog(parent,"Set Input Parameters",info)
    result=dlg.ShowModal()
    
    if result == 'ok':

        for k in keys:
            params[k]=info[k]
        
    else:
        pass
    
    dlg.Destroy()
        
    if not parent:
        app.Run()


