from waxy import *
from mywaxy import *

import pdb


def set_parameter_structure(params,parent=None):
    

    dlg=MessageDialog(parent,
                  text="This feature is for advanced users only.  It is here as a convenience, and can possibly crash the program..  Do you want to continue?",
                  title="Edit the Parameter Structure...", ok=0, yes_no=1,
                  icon='warning')
    result=dlg.ShowModal()
    dlg.Destroy()
    if result != "yes":
        return
    
    pdb.set_trace()
    
    
