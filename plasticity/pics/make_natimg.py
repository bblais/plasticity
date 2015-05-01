#!/usr/bin/env python

import sys
import copy
import glob
import numpy
import Image
import os
import zpickle
import h5py
import array
import pil_numpy as pn
from Waitbar import *

# for dog
import scipy.signal as sig
from scipy.io import loadmat

# for whitening
from scipy.fftpack import fft2, fftshift, ifft2, ifftshift
from scipy import real,absolute

def make_raw_vanhateren100():
    fnames=glob.glob('iml/*.iml')
    im_list=[]
    w = Waitbar(True)
    
    for i,filename in enumerate(fnames):
        fin = open( filename, 'rb' )
        s = fin.read()
        fin.close()
        arr = array.array('H', s)
        arr.byteswap()
        img = numpy.array(arr, dtype='uint16').reshape(1024,1536)
        
        im_list.append(img)
        
        w.update((i+1)/100.0)
        print w,
        sys.stdout.flush()
    
    var={'im':im_list,'im_scale_shift':[1.0,0.0]}
    return var
        

def make_raw_olshausen10():

    data=loadmat('olshausen/IMAGES_RAW.mat')
    IMAGES=data['IMAGESr']
    
    im_list=[]
    for i in range(10):
        im=IMAGES[:,:,i].copy()
        im_list.append(im)
    
    var={'im':im_list,'im_scale_shift':[1.0,0.0]}
    
    return var


def make_raw_olshausen10_white():

    data=loadmat('olshausen/IMAGES.mat')
    IMAGES=data['IMAGES']
    
    im_list=[]
    for i in range(10):
        im=IMAGES[:,:,i].copy()
        im_list.append(im)
    
    var={'im':im_list,'im_scale_shift':[1.0,0.0]}
    
    return var

def make_raw_new_images12(show=True):
    
    files=glob.glob('myimages/new_images12*.png')
    files.sort()
    
    im_list=[]
    
    print "Image files: "
    print files
    
    
    for fname in files:
    
        im=Image.open(fname)
        if show:
            im.show(command='display')
        
        a=numpy.asarray(im.getdata(),dtype='B')
        a.shape=im.size[::-1]
    
        im_list.append(a)
        
        
    var={'im':im_list,'im_scale_shift':[1.0,0.0]}
    
    return var
    

def make_raw(animal='cat',show=True):
    
    files=glob.glob('myimages/*.jpg')
    files.sort()
    
    im_list=[]
    
    if animal=='cat': # can be picky about images
#        files=[files[i] for i in [ 0,1,2,3,4,5,29,32,35,36,46,54,57,58,84]]
        files=[files[i] for i in [ 0,1,2,3,4,5,6,10,12,15,17,19,20,29,32,33,35,36,46,38,40,44,54,57,58,60,69,72,80,84]]
    
    print "Image files: %d" % len(files)
    print "Animal:", animal
    w = Waitbar(True)
    
    file_count=len(files)
    for count,fname in enumerate(files):

        im=Image.open(fname)
        orig_size=im.size
        
        
        if animal=='cat':
            new_size=[int(o*60./0.5*5.5/orig_size[0]) for o in orig_size]
        elif animal=='mouse':
            new_size=[int(o*60./7.*13/orig_size[0]) for o in orig_size]
        else:
            raise ValueError
        
        im=im.convert("L")
        
        if fname==files[0]:
            print "Resize: %dx%d --> %dx%d" % (orig_size[0],orig_size[1],
                                                new_size[0],new_size[1])
        im=im.resize(new_size)
        
        if show:
            im.show()
        
        a=numpy.asarray(im.getdata(),dtype='B')
        a.shape=im.size[::-1]
    
        im_list.append(a)
        
        w.update((count+1)/float(file_count))
        print w,
        sys.stdout.flush()
        
    var={'im':im_list,'im_scale_shift':[1.0,0.0]}
    print
    
    return var

def view(fname,which_pics=None):
    import pylab
    import math
    try:
        var=zpickle.load(fname)
    except TypeError:
        var=fname
        
    pylab.figure()
    pylab.show()
    gray=pylab.cm.gray

    total_num_pics=len(var['im'])
    
    if which_pics:
        var['im']=[var['im'][i] for i in which_pics]
    else:
        which_pics=range(len(var['im']))
    
    num_pics=len(var['im'])
    c=math.ceil(math.sqrt(num_pics))
    r=math.ceil(num_pics/c)
    
    for i in range(num_pics):
        pylab.subplot(r,c,i+1)
        pylab.imshow(var['im'][i],cmap=pylab.cm.gray)
        #pylab.pcolor(var['im'][i],cmap=pylab.cm.gray)
        pylab.hold(False)
        pylab.axis('equal')
#        pylab.imshow(var['im'][i],cmap=gray,aspect='preserve')
        pylab.axis('off')
        if i==0:
            pylab.title('%dx%dx%d' % (var['im'][0].shape[0],var['im'][0].shape[1],total_num_pics))
        else:
            pylab.title('%d' % which_pics[i])
        pylab.draw()
    pylab.show()




    
    
def dog(sd1,sd2,size):
    
    v1=numpy.floor((size-1.0)/2.0)
    v2=size-1-v1
    
    y,x=numpy.mgrid[-v1:v2,-v1:v2]
    
    pi=numpy.pi
    
    # raise divide by zero error if sd1=0 and sd2=0
    
    if sd1>0:
        g=1./(2*pi*sd1*sd1)*numpy.exp(-x**2/2/sd1**2 -y**2/2/sd1**2)
        if sd2>0:
            g=g- 1./(2*pi*sd2*sd2)*numpy.exp(-x**2/2/sd2**2 -y**2/2/sd2**2)
    else:
        g=- 1./(2*pi*sd2*sd2)*numpy.exp(-x**2/2/sd2**2 -y**2/2/sd2**2)
    
    return g

def dog_filter(A,sd1=1,sd2=3,size=None,shape='valid',surround_weight=1):
    
    if not size:
        size=2.0*numpy.ceil(2.0*max([sd1,sd2]))+1.0
        
    if sd1==0 and sd2==0:
        B=copy.copy(A)
        return B
    
    g=dog(sd1,sd2,size)

    B=sig.convolve2d(A,g,mode=shape)
    
    return B

def make_norm(var,mu=0,sd=1):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        im2=im.copy()
        
        im2=im2-im2.mean()
        im2=im2/im2.std()
        
        if count==0:
            print "Norm %.1f,%.1f" % (mu,sd)
        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2

def make_dog(var,sd1=1,sd2=3,size=32,shape='valid'):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        orig_size=im.shape
        im2=dog_filter(im*im_scale_shift[0]+im_scale_shift[1],sd1,sd2,size,shape)
        new_size=im2.shape
        
        im2=im2-im2.mean()
        im2=im2/im2.std()
        
        if count==0:
            print "Dog %d,%d: %dx%d --> %dx%d" % (sd1,sd2,
                                                orig_size[0],orig_size[1],
                                                new_size[0],new_size[1])
        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2

def make_log(var):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        im2=numpy.log(im+1.0)
        new_size=im2.shape
        
        im2=im2/im2.std()
        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2


def eqn_images(var,eqn='x'):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        x=im
        im2=eval(eqn)
        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2
    
    


def make_sigmoid(var):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    
    bottom=0.0
    top=5.0
    
    for count,imm in enumerate(var['im']):
        im=imm*im_scale_shift[0]+im_scale_shift[1]
        im2=copy.copy(im)
        im2[im<0]=bottom*(2.0/(1.0+numpy.exp(-2.0*(im[im<0]/bottom)))-1.0)
        im2[im>=0]=top*(2.0/(1.0+numpy.exp(-2.0*(im[im>=0]/top)))-1.0)
        
        new_size=im2.shape

        im2=im2/im2.std()
        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2

def make_pos(var,type='ON',offset=5,min=0):
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    
    for count,imm in enumerate(var['im']):
        im=imm*im_scale_shift[0]+im_scale_shift[1]
        
        im2=copy.copy(im)
        
        if type=='OFF':
            im2=-im2
            
        im2=im2+offset
        im2[im2<min]=min
        
        new_size=im2.shape

        im2_list.append(im2)
        
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    print
    return var2
    
    
def add_noise(var,sd=1.0):
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        orig_size=im.shape
        im2=im*im_scale_shift[0]+im_scale_shift[1]+sd*numpy.random.randn(im.shape[0],im.shape[1])
        
        im2=im2-im2.mean()
        im2=im2/im2.std()
        im2_list.append(im2)
    
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()

    print
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    return var2
    

def make_blur(var,sd=1.0,radius=None):
    
    if not radius:
        radius=sd*3.0
    
    im2_list=[]
    
    im_scale_shift=var['im_scale_shift']
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
        orig_size=im.shape
        im2=dog_filter(im*im_scale_shift[0]+im_scale_shift[1],sd,0,2*radius+1,shape='same')
        new_size=im2.shape
        
        im2=im2-im2.mean()
        im2=im2/im2.std()
        if count==0:
            print "Blur %d,%d: %dx%d --> %dx%d" % (sd,radius,
                                            orig_size[0],orig_size[1],
                                            new_size[0],new_size[1])
        im2_list.append(im2)
    
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()

    print
    
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    return var2



def make_white(var):
    
    im_scale_shift=var['im_scale_shift']
    im2_list=[]
    
    
    im_count=len(var['im'])
    
    w = Waitbar(True)
    for count,im in enumerate(var['im']):
    
        im=im-im.mean()+1  # add a little DC to get rid of nans
    
        yf=fftshift(fft2(im*im_scale_shift[0]+im_scale_shift[1]))
        fl=1.0/absolute(yf)
        
        yffl=yf*fl;  
        im2=real(ifft2(ifftshift(yffl)))
        
        im2=im2-im2.mean()
        im2=im2/im2.std()

        if count==0:
            print "Whiten."
        im2_list.append(im2)
    
        w.update((count+1)/float(im_count))
        print w,
        sys.stdout.flush()

    print
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    return var2


    
def make_rot(var,which_angles,more=False):
    
    def radians(deg):
        return deg*numpy.pi/180.0
    
    im_scale_shift=var['im_scale_shift']
    im2_list=[]
    

    for a in which_angles:
        print "Rotate ",a
        im_count=len(var['im'])
        
        w = Waitbar(True)
        for count,imm in enumerate(var['im']):
            im=imm*im_scale_shift[0]+im_scale_shift[1]
            
            orig_size=im.shape
            im=im[:,:orig_size[0]]  # crop to square
            sz=im.shape
            new_size=sz
            
            Im=pn.array2image(im).rotate(a)
            im2=pn.image2array(Im)
            
            
            # assume square images, and worst case (45 deg)
            s=sz[0]
            l=int(numpy.ceil(s/numpy.sqrt(2)))
            i1=int((s-l)/2)
            im2=im2[i1:(i1+l),i1:(i1+l)]
            
            im2=im2-im2.mean()
            im2=im2/im2.std()
    
            if count==0:
                print "Rotate %d: %dx%d --> %dx%d" % (a,
                                            orig_size[0],orig_size[1],
                                            new_size[0],new_size[1])
            im2_list.append(im2)
            
            if more:
                im=imm*im_scale_shift[0]+im_scale_shift[1]
                
                orig_size=im.shape
                im=im[:,-orig_size[0]:]  # crop to square
                sz=im.shape
                new_size=sz
                
                Im=pn.array2image(im).rotate(a)
                im2=pn.image2array(Im)
                
                
                # assume square images, and worst case (45 deg)
                s=sz[0]
                l=int(numpy.ceil(s/numpy.sqrt(2)))
                i1=int((s-l)/2)
                im2=im2[i1:(i1+l),i1:(i1+l)]
                
                im2=im2/im2.std()
                im2=im2-im2.mean()
        
                im2_list.append(im2)
                
                if count==0:
                    print "Rotate more %d: %dx%d --> %dx%d" % (a,
                                                    orig_size[0],orig_size[1],
                                                    new_size[0],new_size[1])
            
            
            w.update((count+1)/float(im_count))
            print w,
            sys.stdout.flush()

        print
        
    var2={'im':im2_list,'im_scale_shift':[1.0,0.0]}
    return var2
        
        
        
        
def set_resolution(var,resolution='uint8'):
    
    if (var['im'][0].dtype.name==resolution):  # already there
        return
    
    sr=var['im'][0].dtype.name  # source resolution
    tr=resolution     # target resolution

    # convert to floats first
    for i in range(len(var['im'])):
        var['im'][i]=var['im'][i].astype(numpy.float)
        var['im'][i]=var['im'][i]*var['im_scale_shift'][0]+var['im_scale_shift'][1]
    var['im_scale_shift']=[1.0,0.0]
    
    if tr==numpy.float:
        return
    
    if tr=='uint8':
        maxval=255.0
    elif tr=='uint16':
        maxval=2**16-1.0
    elif tr=='float':
        return
    else:
        raise ValueError,"I don't know the resolution: %s" % resolution
    

    print "Resolution %s -> %s" % (sr,tr)
    
    mn=numpy.Inf
    mx=-numpy.Inf
    for im in var['im']:
        m=im.min()
        if m<mn:
            mn=m
        m=im.max()
        if m>mx:
            mx=m
        
    d=mx-mn   # difference between min and max
    for i in range(len(var['im'])):
        var['im'][i]=(var['im'][i]-mn)/d*maxval
        var['im'][i]=var['im'][i].astype(resolution)
        
    var['im_scale_shift']=[d/maxval, mn]
    
    
def hdf5_save_images(var,fname):
    f=h5py.File(fname,'w')

    f.attrs['im_scale_shift']=var['im_scale_shift']
    for i,im in enumerate(var['im']):
        f.create_dataset('image%d' % i,data=im)

    f.close()

def hdf5_load_images(fname):
    f=h5py.File(fname,'r')
    var={}
    var['im_scale_shift']=list(f.attrs['im_scale_shift'])
    N=len(f.keys())
    var['im']=[]
    for i in range(N):
        var['im'].append(numpy.array(f['image%d' % i]))

    f.close()

    return var

def hdf5_fname(fname):
    base,ext=os.path.splitext(fname)
    return base+".hdf5"


def save(var,fname):
    print "Writing ",fname
    zpickle.save(var,fname)
    fname=hdf5_fname(fname)
    print "Writing ",fname
    hdf5_save_images(var,fname)


if __name__=="__main__":

    # cat stuff
    imfname='pics/catim081604.pics'
    if not os.path.exists(imfname):
        var_raw=make_raw('cat',show=False)
        save(var_raw,imfname)
        
    var_raw=zpickle.load('pics/catim081604.pics')
#    var_raw['im']=[var_raw['im'][0]]  # for debugging: use 1 image

    imfname='pics/catim081604_norm.pics'
    if not os.path.exists(imfname):
        var=make_norm(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)

    imfname='pics/catim081604_dog.pics'
    if not os.path.exists(imfname):
        var=make_dog(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)

    imfname='pics/catim081604_white.pics'
    if not os.path.exists(imfname):
        var=make_white(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)


    # original new images 
    imfname='pics/new_images12.pics'
    if not os.path.exists(imfname):
        var_raw=make_raw_new_images12(show=False)
        save(var_raw,imfname)

    var_raw=zpickle.load('pics/new_images12.pics')
    
    imfname='pics/new_images12_norm.pics'
    if not os.path.exists(imfname):
        var_norm=make_norm(var_raw)
        set_resolution(var_norm,'uint16')
        save(var_norm,imfname)

    imfname='pics/new_images12_dog.pics'
    if not os.path.exists(imfname):
        var_dog=make_dog(var_raw,1,3,22)
        set_resolution(var_dog,'uint16')
        save(var_dog,imfname)

    imfname='pics/new_images12_white.pics'
    if not os.path.exists(imfname):
        var=make_white(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)

    imfname='pics/new_images12_dog_rot13.pics'
    if not os.path.exists(imfname):
        print imfname
        var=make_rot(var_raw,range(0,180,14))
        var_dog=make_dog(var,1,3,22)
        set_resolution(var_dog,'uint16')
        save(var_dog,imfname)


    # olshausen stuff
    imfname='pics/olshausen10.pics'
    if not os.path.exists(imfname):
        print imfname
        var_raw=make_raw_olshausen10()
        save(var_raw,imfname)
        
    imfname='pics/olshausen10_olswhite.pics'
    if not os.path.exists(imfname):
        var_raw=make_raw_olshausen10_white()
        save(var_raw,imfname)


    var_raw=zpickle.load('pics/olshausen10.pics')
        
    imfname='pics/olshausen10_norm.pics'
    if not os.path.exists(imfname):
        var_norm=make_norm(var_raw)
        set_resolution(var_norm,'uint16')
        save(var_norm,imfname)

    imfname='pics/olshausen10_dog.pics'
    if not os.path.exists(imfname):
        var_dog=make_dog(var_raw,1,3,22)
        set_resolution(var_dog,'uint16')
        save(var_dog,imfname)

    imfname='pics/olshausen10_white.pics'
    if not os.path.exists(imfname):
        var=make_white(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)

    imfname='pics/olshausen10_dog_rot13.pics'
    if not os.path.exists(imfname):
        print imfname
        var=make_rot(var_raw,range(0,180,14))
        var_dog=make_dog(var,1,3,22)
        set_resolution(var_dog,'uint16')
        save(var_dog,imfname)
    
    
    # vanhateren stuff
    imfname='pics/vanhateren100.pics'
    if not os.path.exists(imfname):
        print imfname
        var_raw=make_raw_vanhateren100()
        save(var_raw,imfname)
    
    var_raw=zpickle.load('pics/vanhateren100.pics')
    
    imfname='pics/vanhateren100_norm.pics'
    if not os.path.exists(imfname):
        var_norm=make_norm(var_raw)
        set_resolution(var_norm,'uint16')
        save(var_norm,imfname)

    imfname='pics/vanhateren100_dog.pics'
    if not os.path.exists(imfname):
        var_dog=make_dog(var_raw,1,3,22)
        set_resolution(var_dog,'uint16')
        save(var_dog,imfname)

    imfname='pics/vanhateren100_white.pics'
    if not os.path.exists(imfname):
        var=make_white(var_raw)
        set_resolution(var,'uint16')
        save(var,imfname)
        
        