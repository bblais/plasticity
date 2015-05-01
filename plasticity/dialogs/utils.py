from waxy import *
from mywaxy import *

import zpickle
import os
import numpy

from copy import copy
from copy import deepcopy

def hdf5_load_images(fname):
    import h5py,os
    from numpy import array

    if not os.path.exists(fname):
        raise ValueError,"File does not exist: %s" % fname
    f=h5py.File(fname,'r')
    var={}
    var['im_scale_shift']=list(f.attrs['im_scale_shift'])
    N=len(f.keys())
    var['im']=[]
    for i in range(N):
        var['im'].append(array(f['image%d' % i]))

    f.close()

    return var


def array2image(A,rescale=False):
    
    if rescale:
        mn=A.min()
        mx=A.max()
        
        A=A.astype(numpy.float)
        
        A=(A-mn)/(mx-mn)*255.0
    
    A=A.astype(numpy.uint8)
    
    
    sh=A.shape
    
    A=A.reshape(sh[0],sh[1],1)
    A=A.repeat(3,axis=2)
    
    image = EmptyImage(sh[1],sh[0])
    image.SetData(A.tostring())
    
    return image


def subdict(somedict, somekeys, default=None):
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])

class EmptyFrame(Frame):
    
    def __init__(self):
        Frame.__init__(self,None,'',size=(0,0))
    
        self.Hide()
        
    def Body(self):
        self.Close()

        
