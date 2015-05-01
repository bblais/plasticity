from waxy import *
from mywaxy import *

from utils import *

def default_spatial_frequency(params):

    pi=3.141592653589793235
    learning_rule=params['weight_modification'][0]['type']
    if learning_rule in [1,2]: # BCM , Law/Cooper
        k=4.4/13.0*pi
    elif learning_rule==3: # Hebb
        k=1.8/13.0*pi
    else:
        k=4.4/13.0*pi

    return k
       
def get_modification_rule(params):    
    mod_type=params['type']
    
    if isinstance(mod_type,int):
    
        found=[rule for rule in 
                params['rules'] 
                if rule['type']==mod_type][0]
    else:
        found=[rule for rule in 
                params['rules'] 
                if rule['name']==mod_type][0]
    
    return found
       
def get_weight_params(params):
    mod_type=params['type']
    
    if isinstance(mod_type,int):
    
        weight_params=[rule['params'] for rule in 
                params['rules'] 
                if rule['type']==mod_type][0]
    else:
        weight_params=[rule['params'] for rule in 
                params['rules'] 
                if rule['name']==mod_type][0]
    
    return weight_params

class Learning_Rule_Parameters_Dialog(Dialog):
    
    def __init__(self,parent=None,title="Learning Rule Parameters",info=None):

        self.info=info
        self.modification=info['weight_modification']
        Dialog.__init__(self,parent,title)
    
    def Nop(self,event):
        pass
    

    def AddHeading(self,parent,txt):
        
        l=Label(parent,txt,align='c')
        f=Font(l.GetFont().GetFaceName(),12,bold=1,underline=1)
        l.SetFont(f)
        
        parent.AddComponent(l,align='c',expand='h')

    def AddLabel(self, parent, col, row, text, align=None):
        label = Label(parent, text)
        parent.AddComponent(col, row, label, expand=0, align=align or 'vr')
        # note: expand=0 allows us to align the label properly.
        # in this case, 'v' centers it vertically, and 'r' aligns it to
        # the right.

    def Body(self):
        layer=0
    
        panel=Panel(self,direction='vertical')

        rule=get_modification_rule(self.modification[layer])
        mod_type=rule['type']
        weight_params=rule['params']
        
        self.mtype=mod_type
        
        type_str=rule['name']
        self.AddHeading(panel,type_str)
        

        self.params=weight_params
        params_names=self.params.keys()
        params_names.sort()
        
        
        p = FlexGridPanel(self, rows=len(params_names), cols=2, hgap=2, vgap=2)
        self.textbox={}
        
        for i,name in enumerate(params_names):
            
            self.AddLabel(p,0,i,name)
            self.textbox[name]=TextBox(p,str(self.params[name]))
            p.AddComponent(1, i, self.textbox[name])
            
        
        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')
        
        panel.Pack()
    
        self.AddComponent(panel, expand='both', border=3)

    
    

class Weight_Parameters_Dialog(Dialog):
    
    def __init__(self,parent=None,title="",info=None):

        self.info=info
        self.initial_weight_range=info['initial_weight_range']
        self.modification=info['weight_modification']
        self.stabilization=info['weight_stabilization']
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

        self.AddHeading(panel,"Weight Initialization")
        
        p = FlexGridPanel(panel, rows=2, cols=2, hgap=2, vgap=2)

        
        self.AddLabel(p,0,0,"Initial Minimum")
        self.textbox_initial_min=TextBox(p,str(self.initial_weight_range[0]))
        p.AddComponent(1, 0, self.textbox_initial_min)
        
        self.AddLabel(p,0,1,"Initial Maximum")
        self.textbox_initial_max=TextBox(p,str(self.initial_weight_range[1]))
        p.AddComponent(1, 1, self.textbox_initial_max)
        
        
        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')

        line = Line(panel, size=(20,-1), direction='horizontal')
        panel.AddComponent(line, expand='h', border=3)        
        
        self.AddHeading(panel,"Weight Modification")
        
        p = FlexGridPanel(panel, rows=4, cols=2, hgap=2, vgap=2)

        layer=0
        
        
        
        choices=[r['name'] for r in self.modification[layer]['rules']]
        self.mtype_dropdown=DropDownBox(p,choices)
        self.mtype_dropdown.SetSelection(self.modification[layer]['type'])
        self.mtype_dropdown.OnSelect=self.Modification_Type

        self.AddLabel(p,0,0,"Learning Rule")
        p.AddComponent(1, 0, self.mtype_dropdown)

        rule=get_modification_rule(self.modification[layer])
        mod_type=rule['type']
        weight_params=rule['params']
        
        im=rule['image']
        self.mtype_image=Label(p,im,size=(250,50))
#         try:
#             fname=weight_params['image']
#     
#             if not fname:
#                 fname='none'
#         except KeyError:
#             fname='none'
#             
#         self.base_dir=os.path.dirname(__file__)
#         if not self.base_dir:
#             self.base_dir='.'
# 
#         fname=self.base_dir+'/images/learning_rules/'+fname+'.png'
#         
#         self.mtype_image=ImagePanel(p,fname,size=(250,50))
        p.AddComponent(1, 1, self.mtype_image)
        
        
        
        self.mparams_button=Button(p,"Learning Rule Params",
                                   event=self.Learning_Rule_Params)
        
        p.AddComponent(1, 2, self.mparams_button)
        
        
        self.AddLabel(p,0,3,"Learning Rate")
        self.textbox_eta=TextBox(p,str(self.info['eta']))
        p.AddComponent(1, 3, self.textbox_eta)
        
        
        
        
        
        
        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')
        
        
        line = Line(panel, size=(20,-1), direction='horizontal')
        panel.AddComponent(line, expand='h', border=3)        

        self.AddHeading(panel,"Weight Stabilization")
        
        p = FlexGridPanel(panel, rows=4, cols=2, hgap=2, vgap=2)

        layer=0
        
        choices=['None','Oja Normalization','Strict Normalization','Saturation','Weight Decay','Saturation w/o Zero Crossing','Saturation w/ Decay','All Positive Normalization',
        'Saturated with Normalization Per Channel']
        self.stype_dropdown=DropDownBox(p,choices)
        self.stype_dropdown.SetSelection(self.stabilization[layer]['type'])
        self.stype_dropdown.OnSelect=self.Stabilization_Type

        p.AddComponent(1, 0, self.stype_dropdown)

        
        
        self.AddLabel(p,0,1,"Bottom")
        self.textbox_bottom=TextBox(p,str(self.stabilization[layer]['bottom']))
        p.AddComponent(1, 1, self.textbox_bottom)
        
        self.AddLabel(p,0,2,"Top")
        self.textbox_top=TextBox(p,str(self.stabilization[layer]['top']))
        p.AddComponent(1, 2, self.textbox_top)
        
        self.AddLabel(p,0,3,"Decay")
        self.textbox_decay=TextBox(p,str(self.stabilization[layer]['decay']))
        p.AddComponent(1, 3, self.textbox_decay)
        
        
        p.Pack()
        panel.AddComponent(p, expand='h', border=10,align='c')
        
        
        
        panel.Pack()
        
        self.AddComponent(panel, expand='both', border=3)
        

        self.Modification_Type()
        self.Stabilization_Type()
        
    def Modification_Type(self,event=None):
        layer=0
        
        if event:
            self.modification[layer]['type']=event.GetSelection()
            rule=get_modification_rule(self.modification[layer])
            mod_type=rule['type']
            weight_params=rule['params']

            im=rule['image']
            self.mtype_image.SetLabel(str(im))
            
#             try:
#                 fname=weight_params['image']
#         
#                 if not fname:
#                     fname='none'
#             except KeyError:
#                 fname='none'
#             
#             self.base_dir=os.path.dirname(__file__)
#             if not self.base_dir:
#                 self.base_dir='.'
# 
#             fname=self.base_dir+'/images/learning_rules/'+fname+'.png'
#             
#             #fname='images/learning_rules/'+fname+'.png'
#         
#             self.mtype_image.SetImage(fname)

            
    def Learning_Rule_Params(self,event=None):
        layer=0
        
        if event:
            rule=get_modification_rule(self.modification[layer])
            mod_type=rule['type']
            weight_params=rule['params']

            params=weight_params
            
            if not params:
                dlg = MessageDialog(self, "No Parameters",
                "There are no editable parameters for this learning rule",
                icon='information')
                dlg.ShowModal()
                dlg.Destroy()

                return
            
            info={}
            info['weight_modification']=self.modification
                
            dlg=Learning_Rule_Parameters_Dialog(self,"Learning Rule Parameters",info)
            result=dlg.ShowModal()
            
            if result == 'ok':
    
                params_names=params.keys()
                for name in params_names:
                    
                    params[name]=eval(dlg.textbox[name].GetValue())
            
            dlg.Destroy()
            

            
            
            

    def Stabilization_Type(self,event=None):
        layer=0
        
        if event:
            self.stabilization[layer]['type']=event.GetSelection()

        textboxes=[self.textbox_bottom,self.textbox_top,self.textbox_decay]
        
        if self.stabilization[layer]['type']<3: # none, oja, strict
            enable=[0,0,0]
        elif self.stabilization[layer]['type']==3: # saturation
            enable=[1,1,0]
        elif self.stabilization[layer]['type']==4: # decay
            enable=[0,0,1]
        elif self.stabilization[layer]['type']==5: # saturation w/o zero
            enable=[1,1,0]
        elif self.stabilization[layer]['type']==6: # saturation w/decay
            enable=[1,1,1]
        elif self.stabilization[layer]['type']==7: # norm pos
            enable=[0,0,0]
        elif self.stabilization[layer]['type']==8: # sat+norm  channel
            enable=[1,1,1]
            
        for e,box in zip(enable,textboxes):
            if e:
                box.Enable(True)
            else:
                box.Enable(False)
        

    def AddLabel(self, parent, col, row, text, align=None):
        label = Label(parent, text)
        parent.AddComponent(col, row, label, expand=0, align=align or 'vr')
        # note: expand=0 allows us to align the label properly.
        # in this case, 'v' centers it vertically, and 'r' aligns it to
        # the right.
    
    
    
def set_weight_parameters(params,parent=None):
    

    keys=['weight_modification', 
          'weight_stabilization',
          'initial_weight_range',
          'eta']
    
    
    info=deepcopy(subdict(params,keys))
    
    if not parent:
        app = Application(EmptyFrame)
        
    dlg=Weight_Parameters_Dialog(parent,"Set Weight Parameters",info)
    result=dlg.ShowModal()
    
    if result == 'ok':

        layer=0

        eta=float(dlg.textbox_eta.GetValue())
        mn=float(dlg.textbox_initial_min.GetValue())
        mx=float(dlg.textbox_initial_max.GetValue())
        
        modification=info['weight_modification']
        modification[layer]['type']=int(dlg.mtype_dropdown.GetSelection())
        

        stabilization=info['weight_stabilization']
        stabilization[layer]['type']=int(dlg.stype_dropdown.GetSelection())
        stabilization[layer]['top']=float(dlg.textbox_top.GetValue())
        stabilization[layer]['bottom']=float(dlg.textbox_bottom.GetValue())
        stabilization[layer]['decay']=float(dlg.textbox_decay.GetValue())
        
        info['weight_modification']=modification
        info['weight_stabilization']=stabilization
        info['initial_weight_range']=[mn,mx]
        info['eta']=eta
        
        
        for k in keys:
            params[k]=info[k]

        layer=0
        params['test_stimulus'][layer]['k']=default_spatial_frequency(params)
        
    else:
        pass
    
    dlg.Destroy()
        
    if not parent:
        app.Run()
