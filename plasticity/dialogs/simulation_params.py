from waxy import *
from mywaxy import *

from utils import *

class Simulation_Parameters_Dialog(Dialog):
    
    def __init__(self,parent=None,title="",info=None):
        
        self.info=info
        Dialog.__init__(self,parent,title)
    
    
    def Body(self):
    
        p = FlexGridPanel(self, rows=6, cols=2, hgap=2, vgap=2)
        self.AddLabel(p,0,0,"Epoch Number")
        self.textbox_epoch_number=TextBox(p,str(self.info['epoch_number']))
        p.AddComponent(1, 0, self.textbox_epoch_number)

        self.AddLabel(p,0,1,"Iterations Per Epoch")
        self.textbox_iter_per_epoch=TextBox(p,str(self.info['iter_per_epoch']))
        p.AddComponent(1, 1, self.textbox_iter_per_epoch)

        self.AddLabel(p,0,2,"Epochs Per Display")
        self.textbox_epoch_per_display=TextBox(p,str(self.info['epoch_per_display']))
        p.AddComponent(1, 2, self.textbox_epoch_per_display)

        self.AddLabel(p,0,3,"Random Seed")
        self.textbox_random_seed=TextBox(p,str(self.info['random_seed']))
        p.AddComponent(1, 3, self.textbox_random_seed)

        self.checkbox_keep_every_epoch=CheckBox(p,"Keep Every Epoch")
        self.checkbox_keep_every_epoch.SetValue(self.info['keep_every_epoch'])
        p.AddComponent(1,4,self.checkbox_keep_every_epoch)
        
        self.checkbox_save_input=CheckBox(p,"Save Input Vectors")
        self.checkbox_save_input.SetValue(self.info['save_input'])
        p.AddComponent(1,5,self.checkbox_save_input)
        
        p.Pack()
        self.AddComponent(p, expand='both', border=3)

    def AddLabel(self, parent, col, row, text, align=None):
        label = Label(parent, text)
        parent.AddComponent(col, row, label, expand=0, align=align or 'vr')
        # note: expand=0 allows us to align the label properly.
        # in this case, 'v' centers it vertically, and 'r' aligns it to
        # the right.

def set_simulation_parameters(params,parent=None):
    
    keys=['epoch_number', 
          'iter_per_epoch', 
          'epoch_per_display',
          'random_seed', 
          'keep_every_epoch',  
          'save_input']
    
    
    info=deepcopy(subdict(params,keys))
    
    if not parent:
        app = Application(EmptyFrame)
        
    dlg=Simulation_Parameters_Dialog(parent,"Set Simulation Parameters",info)
    result=dlg.ShowModal()
    
    if result == 'ok':
        
        info['epoch_number']=int(dlg.textbox_epoch_number.GetValue())
        info['iter_per_epoch']=int(dlg.textbox_iter_per_epoch.GetValue())
        info['epoch_per_display']=int(dlg.textbox_epoch_per_display.GetValue())
        info['random_seed']=dlg.textbox_random_seed.GetValue()
        
        try:
            info['random_seed']=int(info['random_seed'])
        except ValueError:
            info['random_seed']='clock'
            
            
        info['keep_every_epoch']=int(dlg.checkbox_keep_every_epoch.GetValue())
        info['save_input']=int(dlg.checkbox_save_input.GetValue())
        
        for k in keys:
            params[k]=info[k]
        
    else:
        pass
    
    dlg.Destroy()
        
    if not parent:
        app.Run()
