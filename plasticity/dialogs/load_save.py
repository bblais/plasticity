from waxy import *
from mywaxy import *

from utils import *
import os

def export_fig(parent,filename=None):
    from matplotlib.backends.backend_pdf import FigureCanvasPdf
    
    if not filename:
    
        parent.canvas.Show(False)
            
        dlg = FileDialog(parent, "Export to...",default_dir=os.getcwd(),
                        wildcard='PNG Files|*.png|PDF Files|*.pdf|EPS Files|*.eps|SVG Files|*.svg|All Files|*.*',save=1)
        result = dlg.ShowModal()
        if result == 'ok':
            filename = dlg.GetPaths()[0]
        else:
            filename=None

        filter_index=dlg.GetFilterIndex()
            
        dlg.Destroy()

        parent.canvas.Show(True)
        
        
    if filename:
    
        nme,ext=os.path.splitext(filename)
        if not ext:  # do the filter index
            ext='.pdf'
            
            print filter_index
            
            if filter_index==0:
                ext='.png'
            elif filter_index==1:
                ext='.pdf'
            elif filter_index==2:
                ext='.eps'
        
            filename=nme+ext
    
        nme,ext=os.path.splitext(filename)

        if os.path.exists(filename):
            dlg = MessageDialog(parent, '"%s" already exists. Do you want to replace it?' % filename,
            'A file or folder with the same name already exists in plasticity. Replacing it will overwrite its current contents.',icon='warning',cancel=1)
            result = dlg.ShowModal()
            
            if result=='cancel':
                return
        
        if ext=='.pdf': # hack to fix a problem in the pdf backend
            orig_dpi = parent.fig.dpi.get()
            canvas_pdf = FigureCanvasPdf(parent.fig)
            parent.fig.savefig(filename)
            parent.fig.set_canvas(parent.canvas)  # restore automagically switched attributes
            parent.fig.dpi.set(orig_dpi)
        else:
            parent.fig.savefig(filename)


def save_parameters_as(params,parent=None,filename=None):
    
    if not filename:
    
        if not parent:
            app = Application(EmptyFrame)
        else:
            parent.canvas.Show(False)
            
        dlg = FileDialog(parent, "Save Parameters As...",default_dir=os.getcwd(),
                        wildcard='DAT Files|*.dat|All Files|*.*',save=1)
        result = dlg.ShowModal()
        if result == 'ok':
            filename = dlg.GetPaths()[0]
        else:
            filename=None
            
        dlg.Destroy()

        if not parent:
            app.Run()
        else:
            parent.canvas.Show(True)
            
    params['initial_weights']=[]        
    params['initial_moments']=[]        
    if filename:
        d={'params':params}
        zpickle.save(d,filename)
        
    
def load_parameters(filename=None,parent=None):
    
    
    if not filename:
        if not parent:
            app = Application(EmptyFrame)
        else:
            parent.canvas.Show(False)

        dlg = FileDialog(parent, "Load Parameters",default_dir=os.getcwd(),
                        wildcard='DAT Files|*.dat|All Files|*.*')
        result = dlg.ShowModal()
        if result == 'ok':
            filename = dlg.GetPaths()[0]
        dlg.Destroy()
        if not parent:
            app.Run()
            app.Destroy()
        else:
            parent.canvas.Show(True)

        if result=='cancel':
            return None
        
    params=None
    d=None
    try:
        d=zpickle.load(filename)
    except:
        if not parent:
            app = Application(EmptyFrame)
        dlg = MessageDialog(parent, "Error",
                "Could not load %s" % filename,icon='error')
        dlg.ShowModal()
        dlg.Destroy()
        if not parent:
            app.Run()
            app.Destroy()

    if d:
        try:
            params=d['params']
        except KeyError:
            if not parent:
                app = Application(EmptyFrame)
            dlg = MessageDialog(parent, "Error",
                    "Not a valid parameter file: %s" % filename,icon='error')
            dlg.ShowModal()
            dlg.Destroy()
            if not parent:
                app.Run()
                app.Destroy()
    

    params['load_sim_file']=None
    
    return params
