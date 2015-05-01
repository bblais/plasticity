from waxy import *
from mywaxy import *

from utils import *


class Output_Parameters_Dialog(Dialog):
    
    def __init__(self,parent=None,title="",info=None):
        
        self.info=info
        Dialog.__init__(self,parent,title)
    
    def Nop(self,event):
        pass
    
    def AddHeading(self,parent,txt):
        
        l=Label(parent,txt,align='c')
        f=Font(l.GetFont().GetFaceName(),12,bold=1,underline=1)
        l.SetFont(f)
        
        parent.AddComponent(l,align='c',expand='h')

    def Body(self):
        
        panel=Panel(self,direction='vertical')

        self.AddHeading(panel,"Moments")
        
        p = FlexGridPanel(panel, rows=3, cols=2, hgap=2, vgap=2)

        self.AddLabel(p,0,0,"Tau")
        self.textbox_tau=TextBox(p,str(self.info['tau']))
        p.AddComponent(1, 0, self.textbox_tau)
        
        self.AddLabel(p,0,1,"Initial Minimum")
        self.textbox_initial_min=TextBox(p,str(self.info['initial_moment_range'][0]))
        p.AddComponent(1, 1, self.textbox_initial_min)
        
        self.AddLabel(p,0,2,"Initial Maximum")
        self.textbox_initial_max=TextBox(p,str(self.info['initial_moment_range'][1]))
        p.AddComponent(1, 2, self.textbox_initial_max)
        
        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')
        
        
        self.AddHeading(panel,"Output")
        
        p = FlexGridPanel(panel, rows=6, cols=2, hgap=2, vgap=2)

        layer=0
        
        choices=['Linear','Tanh','Piecewise-linear','Exponential']
        self.type_dropdown=DropDownBox(p,choices)
        self.type_dropdown.SetSelection(self.info['output'][layer]['type'])
        self.type_dropdown.OnSelect=self.Output_Type

        p.AddComponent(1, 0, self.type_dropdown)

        self.AddLabel(p,0,1,"Bottom")
        self.textbox_bottom=TextBox(p,str(self.info['output'][layer]['bottom']))
        p.AddComponent(1, 1, self.textbox_bottom)

        self.AddLabel(p,0,2,"Top")
        self.textbox_top=TextBox(p,str(self.info['output'][layer]['top']))
        p.AddComponent(1, 2, self.textbox_top)

        self.AddLabel(p,0,3,"Exponential Scale")
        self.textbox_scale=TextBox(p,str(self.info['output'][layer]['scale']))
        p.AddComponent(1, 3, self.textbox_scale)

        self.AddLabel(p,0,4,"Sigma Tau")
        self.textbox_sigma_tau=TextBox(p,str(self.info['output'][layer]['sigma_tau']))
        p.AddComponent(1, 4, self.textbox_sigma_tau)

        self.AddLabel(p,0,5,"Sigma_o")
        self.textbox_sigma_o=TextBox(p,str(self.info['output'][layer]['sigma_o']))
        p.AddComponent(1, 5, self.textbox_sigma_o)



        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')
        
        panel.Pack()
        
        self.AddComponent(panel, expand='both', border=3)
        
        self.Output_Type()

    def Output_Type(self,event=None):
        layer=0
        
        if event:
            self.info['output'][layer]['type']=event.GetSelection()

        if self.info['output'][layer]['type']==0: # linear
            self.textbox_bottom.Enable(False)
            self.textbox_top.Enable(False)
        else:
            self.textbox_bottom.Enable(True)
            self.textbox_top.Enable(True)
        
        

    def AddLabel(self, parent, col, row, text, align=None):
        label = Label(parent, text)
        parent.AddComponent(col, row, label, expand=0, align=align or 'vr')
        # note: expand=0 allows us to align the label properly.
        # in this case, 'v' centers it vertically, and 'r' aligns it to
        # the right.
    
    
    
def set_output_parameters(params,parent=None):
    

    keys=['output', 
          'tau',
          'initial_moment_range']
    
    
    info=deepcopy(subdict(params,keys))
    
    
    if not parent:
        app = Application(EmptyFrame)
        
    dlg=Output_Parameters_Dialog(parent,"Set Output Parameters",info)
    result=dlg.ShowModal()
    
    if result == 'ok':

        mn=float(dlg.textbox_initial_min.GetValue())
        mx=float(dlg.textbox_initial_max.GetValue())
        tau=float(dlg.textbox_tau.GetValue())
        
        layer=0
        info['output'][layer]['type']=int(dlg.type_dropdown.GetSelection())
        info['output'][layer]['top']=float(dlg.textbox_top.GetValue())
        info['output'][layer]['bottom']=float(dlg.textbox_bottom.GetValue())
        info['output'][layer]['sigma_o']=float(dlg.textbox_sigma_o.GetValue())
        info['output'][layer]['scale']=float(dlg.textbox_scale.GetValue())
        info['output'][layer]['sigma_tau']=float(dlg.textbox_sigma_tau.GetValue())
        info['initial_moment_range']=[mn,mx]
        info['tau']=tau

        for k in keys:
            params[k]=info[k]
    else:
        pass
    
    dlg.Destroy()
        
    if not parent:
        app.Run()


