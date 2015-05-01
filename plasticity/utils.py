import math
import copy
import numpy
import zpickle
from numpy import exp,array
from Struct import Struct

def hdf5_load_images(fname):
    import h5py,os
    
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


def scale_shift_filter(image,scale=1.0,shift=0.0,truncate=False):
    
    for im in image:
        
        im[:]=scale*im+shift

        if truncate:
            im[im<0]=0.0
        
        
def ON_filter(image,offset=5,truncate=False,norm=False):
    for im in image:
        
        
        im[:]=im+offset
        
        if truncate:
            im[im<0]=0.0
        
        
        if norm:
            im[:]=im/max(im.flat)*5.0


def get_test_stimulus():
    params={}
    params['type']=0  # none
    params['type']=1  # test_OR_single
    params['numang']=24;
    params['k']=4.4/13.0*3.141592653589793235;
  
    return params

def array2var(a):
    
    var={}
    var={'im':[numpy.asarray(a,numpy.float64)],'im_scale_shift':[1.0,0.0]}
    return var

       

def get_noise(type=0,mean=0,std=1,min=-1e500):

    # types:
    #  0: none
    #  1: uniform
    #  2: gaussian
    #  3: laplace

    typedict={0:0,'none':0,
              1:1,'uniform':1,
              2:2,'gaussian':2,
              3:3,'laplace':3,
              4:4,'proportional':4,
              }
                
    
    params={}
    params['type']=typedict[type]
    params['mean']=mean
    params['std']=std
    params['min']=min

    return Struct(params)
       
def get_pattern(type=2,scale=1.0,filename='hdf5/new_images12_dog.hdf5',
                var=[],num_inputs=169,masktype='circle',mask=[],
                filter=None):

    # types:
    #  0: none
    #  1: data vectors
    #  2: images

    params={}
    params['type']=type
    params['scale']=scale
    params['var']=var
    params['filter']=filter
    params['filter_params']=Struct({})
    params['sequential']=False
    
    if not params['var']:
        params['filename']=filename
        params['masktype']=masktype
    else:
        params['filename']=''
        params['masktype']='none'
        if not filter is None:
            params['filter'](var)
        
    params['num_inputs']=num_inputs

    params['pattern_probability']=1.0
    params['non_pattern_noise']=get_noise()
        
    # mask types:
    # circle
    # none
    # user
    
    params['mask']=mask

    return Struct(params)

def get_feedback(type=0,l=1,file='',var=[],num_cycles=1):

    # types:
    #  0: none
    #  1: additive
    #  2: multiplicative

    params={}
    params['type']=type
    params['lambda']=l
    params['file']=file
    params['var']=var
    params['num_cycles']=num_cycles

    return Struct(params)
       
def get_lateral(type=0,file='',var=[],num_cycles=1):

    # types:
    #  0: none
    #  1: gramm-schmidt orthogonalization - var is orth weights
    #  2: symmetric orthogonalization
    #  3: matrix
    #  4: uniform, modifiable

    params={}
    params['type']=type
    params['file']=file
    params['var']=var
    params['num_cycles']=num_cycles

    return Struct(params)
       

def get_output(type=1,bottom=-1,top=50,
                sigma_o=1,sigma_tau=0,scale=1,
                weight_offset=0.0,
                mean_weight_offset=0.0,
                output_noise=None):

    # types:
    #  0: linear
    #  1: sigmoid
    #  2: piecewise-linear
    #  3: exponential

    params={}
    params['type']=type
    params['use_derivative']=False
    params['top']=top
    params['bottom']=bottom
    params['scale']=scale  # for exponential
    params['sigma_o']=sigma_o
    params['sigma_tau']=sigma_tau
    params['weight_offset']=weight_offset
    params['mean_weight_offset']=weight_offset
    params['output_noise']=get_noise()
    
    return Struct(params)

    

def add_rule(rules,name,image,params,type=None):
    try:
        mx=max([r['type'] for r in rules])
    except ValueError: #empty rules
        mx=-1
        
    rule={}
    if type is None:
        rule['type']=mx+1
    else:
        rule['type']=type
        
    rule['name']=name
    rule['image']=image
    rule['params']=params
    
    rules.append(Struct(rule))

def get_modification_rule(params):    
    mod_type=params['weight_modification'][0]['type']
    
    if isinstance(mod_type,int):
    
        found=[rule for rule in 
                params['weight_modification'][0]['rules'] 
                if rule['type']==mod_type][0]
    else:
        found=[rule for rule in 
                params['weight_modification'][0]['rules'] 
                if rule['name']==mod_type][0]
    
    return found
    
def get_num_moments(params):
    
    num_moments=1
        
    weight_params=get_weight_params(params)
    
    if 'tau_beta' in weight_params:
        if weight_params['tau_beta']>0:
            num_moments+=1
            
    if get_modification_rule(params)['type']==31:  # BCM8292
        num_moments+=1

    if get_modification_rule(params)['type']==32:  # Law/Cooper BCM with Lower dynamic threshold
        num_moments+=1
    if get_modification_rule(params)['type']==33:  # Law/Cooper BCM with Lower dynamic threshold
        num_moments+=1
        
    return num_moments
    
    
def get_weight_params(params):
    mod_type=params['weight_modification'][0]['type']
    
    if isinstance(mod_type,int):
    
        weight_params=[rule['params'] for rule in 
                params['weight_modification'][0]['rules'] 
                if rule['type']==mod_type][0]
    else:
        weight_params=[rule['params'] for rule in 
                params['weight_modification'][0]['rules'] 
                if rule['name']==mod_type][0]
    
    return weight_params

def get_weight_modification(type=1):

    # types:
    #  0: none
    #  1: bcm
    #  2: law/cooper bcm
    #  3: hebb
    #  4: user1

    params={}
    params['type']=type
    
    rules=[]
    
    add_rule(rules,'None',None,{})
    add_rule(rules,'BCM','dw/dt=eta*y(y-th) x',{'tau_beta':0,
        'linear_beta':True,'k_beta':1.0})
    add_rule(rules,'Law/Cooper BCM','dw/dt=eta*y(y-th)/th x',{'tau_beta':0,
        'linear_beta':True,'k_beta':1.0})
    add_rule(rules,'Hebb','dw/dt=eta*y*x',{})
    add_rule(rules,'User1',None,{'theta_o':3,'a':1,'b':0,'c':0})
    add_rule(rules,'User2',None,{'theta_o':3,'a':1,'b':0,'c':0})
    add_rule(rules,'Unified Presyn',None,
                        {'theta_o':1,'theta_p':3,'decay':1})
    add_rule(rules,'Unified 2',None,
                        {'theta_o':1,'theta_p':3,'decay':1})
    add_rule(rules,'Modified Spontaneous',None,
                        {'sigma_o':1,'sigma_tau':0})

    for i in range(1,13):
        add_rule(rules,'Rule #%d' % i,None,{'tau_beta':0,
        'linear_beta':True,'k_beta':1.0})
        
    add_rule(rules,'Individual Thresholds #1',None,{'tau_beta':0,
        'linear_beta':True,'k_beta':1.0})

    add_rule(rules,'Rule #7a', 
            'eta*(x^2*y^2)*(y-th)*x/th (Rule 7 with Charlie)',
            {'tau_beta':0,
        'linear_beta':True,'k_beta':1.0},type=22)
    add_rule(rules,'Rule #7b', 
            'eta*(x^2*y^2)*(y-th)*x/th^2 (Rule 7 with Charlie^2)',
            {'tau_beta':0,
        'linear_beta':True,'k_beta':1.0},type=23)

    add_rule(rules,'Rule #6a', 
            'eta*y(y-th)*x^2/th (Rule 6 with Charlie)',
            {'tau_beta':0,
        'linear_beta':True,'k_beta':1.0},type=24)
    add_rule(rules,'Rule #6b', 
            'eta*y(y-th)*x^2/th^2 (Rule 6 with Charlie^2)',
            {'tau_beta':0,
        'linear_beta':True,'k_beta':1.0},type=25)

    # None == 0
    # BCM == 1
    # Law/Cooper BCM == 2
    # Hebb == 3
    # User1 == 4
    # User2 == 5
    # Unified Presyn == 6
    # Unified 2 == 7
    # Modified Spontaneous == 8
    # Rule #1 == 9
    # Rule #2 == 10
    # Rule #3 == 11
    # Rule #4 == 12
    # Rule #5 == 13
    # Rule #6 == 14
    # Rule #7 == 15
    # Rule #8 == 16
    # Rule #9 == 17
    # Rule #10 == 18
    # Rule #11 == 19
    # Rule #12 == 20
    # Individual Thresholds #1 == 21

    add_rule(rules,'Law/Cooper BCM w/-gamma*y^2*w',
            'dw/dt=eta*y(y-th)/th x - gamma*y^2*w',
            {'tau_beta':0,'gamma':0,
        'linear_beta':True,'k_beta':1.0},type=26)
    add_rule(rules,'Law/Cooper BCM w/-gamma*y*w',
            'dw/dt=eta*y(y-th)/th x - gamma*y*w',
            {'tau_beta':0,'gamma':0,
        'linear_beta':True,'k_beta':1.0},type=27)

    add_rule(rules,'Law/Cooper BCM w/theta_L',
            'dw/dt=eta*(y-theta_L)(y-th)/th x',
            {'tau_beta':0,'theta_L':1,
        'linear_beta':True,'k_beta':1.0},type=28)

    add_rule(rules,'Law/Cooper BCM w/theta_L fraction',
            'dw/dt=eta*(y-theta_L_fraction*th)(y-th)/th x',
            {'tau_beta':0,'theta_L_fraction':0.1,
        'linear_beta':True,'k_beta':1.0},type=29)

    add_rule(rules,'Log Phi',
            'dw/dt=eta*y*(log (y/theta)) x, theta ~ E[y^(1+gamma)/theta_o^gamma]',
            {'gamma':1,'theta_o':10,
        'linear_beta':True,'k_beta':1.0},type=30)

    add_rule(rules,'BCM8292',
            'dw/dt=eta*y*(y-theta) x, theta ~ E[y^(1+alpha)]^(2-alpha)',
            {'alpha':1,
        'linear_beta':True,'k_beta':1.0},type=31)

    add_rule(rules,'Law/Cooper BCM with Dynamic Lower Threshold', 
            'eta*(y-theta_L)(y-th)*x/th',
            {'tau_beta':0,'tau_theta_L':100,
        'linear_beta':True,'k_beta':1.0},type=32)

    add_rule(rules,'Law/Cooper BCM with Dynamic Lower Threshold 2', 
            'eta*(y-theta_L)(y-th)*x/th',
            {'tau_beta':0,'tau_theta_L':100,'k_theta_L':0.5,
        'linear_beta':True,'k_beta':1.0},type=33)



    params['rules']=rules

    
    return Struct(params)
    
def get_weight_stabilization(type=0,bottom=-1,top=1,decay=1):

    # types:
    #  0: none
    #  1: oja norm
    #  2: strict norm
    #  3: saturation
    #  4: weight decay
    #  5: saturation w/o zero cross
    #  6: saturation w weight decay
    #  7: all positive normalization
    #  8: saturated gerstner normalization
        # i.e. find the norm of channel 1, and make channel 2 the same

    params={}
    params['type']=type
    params['top']=top
    params['bottom']=bottom
    params['decay']=decay

    return Struct(params)



def default_params():

    params={}
    import version
    
    params['version']=version.version
    params['config']={}
    params['epoch_number']=500 
    params['iter_per_epoch']=500
    params['epoch_per_display']=100
    params['minimum_print_time']=0
    params['random_seed']='clock'
    params['random_seed2']=0
    params['actual_random_seed']=0
    params['eta']=8e-6
    params['tau']=1000
    params['initial_weights']=[]
    params['initial_moments']=[]
    params['initial_weight_range']=[-.05, .05]
    params['initial_moment_range']=[.01, .02]
    params['num_neurons']=[1, 1]
    params['neuron_offsets']=[0, 0]
    params['save_input']=0
    params['saved_input_vectors']=[]
    params['save_lateral_matrix']=0
    params['temporal_filter']=[]
    params['pattern_input']= [get_pattern(), get_pattern()]
    params['noise_input']= [get_noise(), get_noise()]
    params['feedback']= [get_feedback()]
    params['output']= [get_output()]
    params['lateral']= [get_lateral()]
    params['weight_saturation']=[ [] ]
    params['weight_stabilization']=[get_weight_stabilization()]
    params['weight_modification']=[get_weight_modification()]
    params['display']=1
    params['display_params']={}
    params['display_module']=None
    params['test_stimulus']=[get_test_stimulus()]
    params['keep_every_epoch']=0
    params['tmpfile']=''
    params['save_sim_file']='untitled.dat'
    params['continue']=0
    params['load_sim_file']=''

    
    return Struct(params)

def setminmax(y,yp_mnmx=None,y_mnmx=None):

    if not y_mnmx:
        y_mnmx=[y.min(),y.max()]
    
    if not yp_mnmx:
        yp=copy.copy(y)
        scale=1
        shift=0
    else:
        if (y_mnmx[0]==y_mnmx[1]):
            yp=copy.copy(y)
            scale=1
            shift=0
        else:
            scale=(yp_mnmx[1]-yp_mnmx[0])/(y_mnmx[1]-y_mnmx[0])
            shift=-scale*y_mnmx[0]+yp_mnmx[0]
    
            yp=scale*y+shift
        
            
    return yp
        
def save_params(params,fname):
    
    zpickle.save(params,fname)
    
    
def load_params(fname):
    
    d=zpickle.load(fname)
    
    if 'epoch_number' in d:
        return d
    else:
        return d['params']
    
    
def load_sim(fname):
    
    d=zpickle.load(fname)
    
    return d    
    
    
    
def weights2eyes(params,weights):

    eyes=[]
    
    num_channels=len(params['pattern_input'])
    inputs_per_channel=params['pattern_input'][0]['num_inputs']
    rfsize=int(math.sqrt(inputs_per_channel))
    
    wim=[]
    
    for k in range(num_channels):
        w=weights[0][0][k*inputs_per_channel:(k+1)*inputs_per_channel]
    
        w=w.reshape(rfsize,rfsize)
        eyes.append(w)
        
    return eyes


def weights2image(params,weights,mnmx=None,buffer_color=255):
    
    num_channels=len(params['pattern_input'])
    total_num_neurons=weights[0].shape[0]
    inputs_per_channel=params['pattern_input'][0]['num_inputs']
    rfsize=int(math.sqrt(inputs_per_channel))
    
    mn=[]
    mx=[]
    for n in range(total_num_neurons):
        for k in range(num_channels):
            w=weights[0][n][k*inputs_per_channel:(k+1)*inputs_per_channel]
            try:
                mask=params['pattern_input'][k]['mask'].ravel()
                mn.append(w[mask==1].min())
                mx.append(w[mask==1].max())
            except AttributeError:  # for an empty mask list
                mn.append(w.min())
                mx.append(w.max())

    mn=min(mn)
    mx=max(mx)
        
    if not mnmx:
        mnmx=[mn, mx]
        
    row=[]
    #buffer_color=255
    n=0
    for ni in range(params['num_neurons'][0]):
        wimn=[]
        for nj in range(params['num_neurons'][1]):
            wim=[]
            for k in range(num_channels):
                w=weights[0][n][k*inputs_per_channel:(k+1)*inputs_per_channel]
            
                w=setminmax(w,[0,255],[mnmx[0],mnmx[1]])
                
                if not params['pattern_input'][k]['mask']==[]:
                    w[params['pattern_input'][k]['mask'].ravel()==0.0]=buffer_color
                
                
                w=w.reshape(rfsize,rfsize)
                wim.append(w)
                if (k<(num_channels-1)):
                    wim.append(buffer_color*numpy.ones((rfsize,3),numpy.float64))
            
            wim=numpy.concatenate(wim,axis=1)
            wimn.append(wim)
        row.append(numpy.concatenate(wimn,axis=1))
    wim=numpy.concatenate(row,axis=0)
        
    return wim
        

def sigmoid(y,bottom,top):

    y[y<0]=bottom*(2.0/(1.0+exp(-2.0*(y[y<0]/bottom)))-1.0)
    y[y>=0]=top*(2.0/(1.0+exp(-2.0*(y[y>0]/top)))-1.0)

def scale_shift_filter(image,scale=1.0,shift=0.0,max=1e500,min=-1e500):
    
    for im in image:
        
        im[:]=scale*im+shift

        im[im<min]=min
        im[im>max]=max
        
def sigmoid_scale_shift_filter(image,scale=1.0,shift=0.0,bottom=-5,top=5):
    
    for im in image:
        
        sigmoid(im,bottom,top)
        im[:]=scale*im+shift

