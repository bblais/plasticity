cimport cython

import numpy as np
cimport numpy as c_numpy

import os
import sys

import zpickle  
import numpy as np
cimport numpy as np
from numpy import array,matrix
from utils import get_modification_rule,hdf5_load_images

cdef int debug=0

cdef extern from "math.h":
    double sqrt(double)
    double exp(double)
    double log(double)
    double tanh(double)
    double pow(double,double)
    
from bbrand cimport init_by_int,init_by_entropy,randu,randn,rande

# to replace randu if needed

# make a buffer of random numbers, and call that.  This makes it so that I can use the same
# random number seed in python and C, and I get most of the speed of C...just need to keep a 
# bunch of numbers handy
cdef int _random_number_buffer_size=10000
cdef int _random_number_index=_random_number_buffer_size
cdef np.ndarray _random_numbers
cdef double randuu():
    global _random_numbers,_random_number_index,_random_number_buffer_size
    if _random_number_index>=_random_number_buffer_size:  # fill the buffer
        if debug:
            print "here"
        _random_numbers=np.random.rand(_random_number_buffer_size)
        _random_number_index=0
        
    cdef double value
    cdef double *_random_numbers_p=<double *> c_numpy.PyArray_DATA(_random_numbers)
    value=_random_numbers_p[_random_number_index]
    _random_number_index+=1
        
    return value




def get_full_mask(params):
    cdef int k,num_inputs,num_channels
    
    # fill in the mask
    full_mask=[]
    num_channels=len(params['pattern_input'])
    for k from 0 <= k < num_channels:
        num_inputs=params['pattern_input'][k]['num_inputs']
        if params['pattern_input'][k]['masktype']=='circle':
            full_mask.append(get_circle_mask(num_inputs))
        elif params['pattern_input'][k]['masktype']=='none':
            full_mask.append(np.ones((1,num_inputs),np.float64))
        else:
            if len(params['pattern_input'][k]['mask'])!=num_inputs:
                raise ValueError,"Mask size is wrong"
            else:
                full_mask.append(params['pattern_input'][k]['mask'].astype(np.float64))

    full_mask=np.array(full_mask).ravel()
    return full_mask

def init_params(params):


    cdef int k,t,i
    cdef int num_channels,num_inputs,rf_size
    
    num_channels=len(params['pattern_input'])
    
    # fill in the variables
    for k from 0 <= k < num_channels:
        if not params['pattern_input'][k]['type']:  # no input
            continue
    
        if not params['pattern_input'][k]['var']:  # empty variable
            if not params['pattern_input'][k]['filename']:  # no filename either
                params['pattern_input'][k]['type']=0
                continue
            
            fname=params['pattern_input'][k]['filename']
            base,ext=os.path.splitext(fname)
            
            if ext=='.pics' or ext=='.dat':
                params['pattern_input'][k]['var']=zpickle.load(fname)
            elif ext=='.hdf5':
                params['pattern_input'][k]['var']=hdf5_load_images(fname)
            else:
                raise ValueError,"Unknown image data extension %s" % ext

            im=params['pattern_input'][k]['var']['im']
            imss=params['pattern_input'][k]['var']['im_scale_shift']

            for i from 0<= i < len(im):
                im[i]=(im[i]*imss[0]+imss[1]).astype(np.float64)
            
            if params['pattern_input'][k]['filter']:
                params['pattern_input'][k]['filter'](im,**params['pattern_input'][k]['filter_params'])
                
    # fill in the mask
    for k from 0 <= k < num_channels:
        num_inputs=params['pattern_input'][k]['num_inputs']
        if params['pattern_input'][k]['masktype']=='circle':
            params['pattern_input'][k]['mask']=get_circle_mask(num_inputs)
        elif params['pattern_input'][k]['masktype']=='none':
            params['pattern_input'][k]['mask']=np.ones((1,num_inputs),np.float64)
        else:
            if len(params['pattern_input'][k]['mask'])!=num_inputs:
                raise ValueError,"Mask size is wrong"
            else:
                params['pattern_input'][k]['mask']=params['pattern_input'][k]['mask'].astype(np.float64)  

    # make the offsets
    for k from 0 <= k < num_channels:
        t=params['pattern_input'][k]['type']                
        num_inputs=params['pattern_input'][k]['num_inputs']                
        params['pattern_input'][k]['offset']=[0,0]
        params['pattern_input'][k]['idx']=[]
        if t==0: # none
            pass
        elif t==1: # data
            im=params['pattern_input'][k]['var']['im'][0]
            params['pattern_input'][k]['max_offset']=[
                    im.shape[0],im.shape[1]-num_inputs]
            params['pattern_input'][k]['idx']=np.arange(num_inputs,dtype=np.int32)
        elif t==2: # images
            im=params['pattern_input'][k]['var']['im'][0]
            rf_size=int(sqrt(num_inputs))
            params['pattern_input'][k]['max_offset']=[
                    im.shape[0]-rf_size,im.shape[1]-rf_size]
                    
            ii=np.arange(num_inputs,dtype=np.int32)
            params['pattern_input'][k]['idx']=(ii%rf_size)+(ii/rf_size)*im.shape[1]
        else:
            raise ValueError,"Bad pattern type" + t

                
def get_circle_mask(int num_inputs):
    
    mask=np.zeros((num_inputs,1),np.float64)
    
    cdef int rf_diameter,it
    
    rf_diameter=int(sqrt(num_inputs))

    i=np.arange(0,num_inputs,dtype=np.int32)
    ii=i%rf_diameter-rf_diameter/2.0+0.5
    jj=i/rf_diameter-rf_diameter/2.0+0.5
    r2=(ii*ii)+(jj*jj)
    
    for it from 0<=it < num_inputs:
        if r2[it]<=(num_inputs/4.0):
            mask[it]=1.0

    return mask    


blah={'offsets':[],
    'pics':[],
    'y':[],
    'phi':[]
    }

def set_offsets(params):

    cdef int k
    
    cdef int num_channels
    num_channels=len(params['pattern_input'])
    
    
    cdef double r1,r2,r3
    cdef int offset,pic,npics
    cdef int sequential
    
    pic=0
    offset=0
    
    r1=randu()
    r2=randu()
    r3=randu()
    
    
    for k from 0<=k<num_channels:
        p=params['pattern_input'][k]
        num_inputs=p['num_inputs']
        t=p['type']
        sequential=p['sequential']
        
        if t==0:  # none
            pass
        elif t==1: # data
            im=params['pattern_input'][k]['var']['im'][0]
            offset=int(r1*p['max_offset'][0])*im.shape[1]+int(r2*p['max_offset'][1])
            pic=0
        elif t==2: # image
            im=params['pattern_input'][k]['var']['im'][0]
            npics=len(params['pattern_input'][k]['var']['im'])
            offset=int(r1*p['max_offset'][0])*im.shape[1]+int(r2*p['max_offset'][1])
            if sequential:
                pic=p['offset'][0]+1
                if pic>=npics:
                    pic=0
            else:
                pic=int(r3*npics)
                
            blah['offsets'].append(offset)
            blah['pics'].append(pic)
        else:
            raise ValueError,"bad pattern type"
            
        p['offset']=[pic,offset]


def set_offsets_systematic(params):

    cdef int k
    
    cdef int num_channels
    num_channels=len(params['pattern_input'])
    
    
    cdef double r1,r2,r3
    cdef int offset,pic,npics,o1,o2
    cdef int sequential
    
    pic=0
    offset=0
    
    r1=randu()
    r2=randu()
    r3=randu()

        
    for pic in range(len(params['pattern_input'][0]['var']['im'])):
        for o1 in range(params['pattern_input'][0]['max_offset'][0]):
            for o2 in range(params['pattern_input'][0]['max_offset'][1]):
    
                for k from 0<=k<num_channels:
                    p=params['pattern_input'][k]
                    num_inputs=p['num_inputs']
                    t=p['type']
                    assert t==2,"systematic type not implemented except for images"
                    
                    sequential=p['sequential']
        
                    im=params['pattern_input'][k]['var']['im'][0]
                    npics=len(params['pattern_input'][k]['var']['im'])
                    offset=o1*im.shape[1]+o2
                    p['offset']=[pic,offset]

                yield 1


            
cdef apply_noise(object n,double *x,double *mask,int num_inputs):
    cdef int t,i
    cdef double mean,std,min
    
    t=n['type']
    
    if t==0: # none
        for i from 0<=i < num_inputs:
            x[i]=x[i]*mask[i]
    elif t==1: # uniform
        mean=n['mean']
        std=n['std']
        for i from 0<=i < num_inputs:
            x[i]=x[i]+(randu()-0.5)*2.0*1.732050807569*std+mean
            x[i]=x[i]*mask[i]
    elif t==2: # gaussian
        mean=n['mean']
        std=n['std']
        min=n['min']
        for i from 0<=i < num_inputs:
            nx=randn()*std+mean
            if nx<min:
                nx=min
            x[i]=x[i]+nx
            x[i]=x[i]*mask[i]
    elif t==3: # laplace
        mean=n['mean']
        std=n['std']
        min=n['min']
        for i from 0<=i < num_inputs:
            
            if randu()>0.5:
                nx=rande()/1.414213562373*std+mean
            else:
                nx=-rande()/1.414213562373*std+mean
            if nx<min:
                nx=min
                             
            x[i]=x[i]+nx
            x[i]=x[i]*mask[i]
    elif t==4: # proportional
        mean=n['mean']
        std=n['std']
        min=n['min']
        for i from 0<=i < num_inputs:
            nx=randn()*std
            if nx<min:
                nx=min
            x[i]=x[i]+(nx*x[i]+mean)
            x[i]=x[i]*mask[i]


def get_systematic_input_vector(c_numpy.ndarray X,params):


    cdef int num_channels,num_neurons,total_num_inputs
    cdef double *x
    cdef double *im
    cdef double *mask
    cdef int *idx
    cdef c_numpy.ndarray Im,Idx,Mask
    cdef double pattern_probability
    
    mask=<double*>0
    
    x=<double *>c_numpy.PyArray_DATA(X)
    
    num_channels=len(params['pattern_input'])
    num_neurons=c_numpy.PyArray_DIMS(X)[0]
    total_num_inputs=c_numpy.PyArray_DIMS(X)[1]

    cdef int t,k,i,count,countn,num_inputs
    cdef double scale
    cdef int offset,npics,pic
    cdef int lenx
    cdef double mean,std,min,nx
    cdef int non_pattern
    
    # TODO: do with offset, right now I just copy the first vector
    
    for i in set_offsets_systematic(params):
        count=0
        countn=0
    
    
        for k from 0<=k<num_channels:
            p=params['pattern_input'][k]

            num_inputs=p['num_inputs']
            t=p['type']
            pattern_probability=p['pattern_probability']
            if randu()>pattern_probability:  # don't apply the pattern
                non_pattern=True
                t=0  # no pattern
            else:
                non_pattern=False  # double negative!  :)
        
            
            if t==0:  # none
                Mask=p['mask']
                mask=<double *>c_numpy.PyArray_DATA(Mask)
                for i from 0<=i < num_inputs:
                    x[count]=0.0
                    count=count+1
                
                if non_pattern:
                    n=p['non_pattern_noise']
                    apply_noise(n,&x[countn],mask,num_inputs)        
                
                
            elif t==1: # data
                pic=p['offset'][0]
                offset=p['offset'][1]
                scale=p['scale']
        
            
                Im=p['var']['im'][pic]
                im=<double *>c_numpy.PyArray_DATA(Im)

                Idx=p['idx']
                idx=<int *>c_numpy.PyArray_DATA(Idx)
            
                Mask=p['mask']
                mask=<double *>c_numpy.PyArray_DATA(Mask)
                        
                for i from 0<=i < num_inputs:
                    x[count]=im[idx[i]+offset]*scale*mask[i]
                    count=count+1

            elif t==2: # image
                pic=p['offset'][0]
                offset=p['offset'][1]
                scale=p['scale']

                Im=p['var']['im'][pic]
                im=<double *>c_numpy.PyArray_DATA(Im)

                Idx=p['idx']
                idx=<int *>c_numpy.PyArray_DATA(Idx)
            
                Mask=p['mask']
                mask=<double *>c_numpy.PyArray_DATA(Mask)
                        
                for i from 0<=i < num_inputs:
                    x[count]=im[idx[i]+offset]*scale
                    count=count+1

            if not non_pattern:   # an actual pattern, even if 0
                # apply the noise
                n=params['noise_input'][k]
                apply_noise(n,&x[countn],mask,num_inputs)        
            
            countn+=num_inputs
        
        # copy the network inputs
        countn=total_num_inputs
        for k from 1<=k<num_neurons:
            for i from 0<=i<total_num_inputs:
                x[countn]=x[i]
                countn+=1

        yield 1
        
    
def get_input_vector(c_numpy.ndarray X,params):


    cdef int num_channels,num_neurons,total_num_inputs
    cdef double *x
    cdef double *im
    cdef double *mask
    cdef int *idx
    cdef c_numpy.ndarray Im,Idx,Mask
    cdef double pattern_probability
    
    mask=<double*>0
    
    x=<double *>c_numpy.PyArray_DATA(X)
    
    num_channels=len(params['pattern_input'])
    num_neurons=c_numpy.PyArray_DIMS(X)[0]
    total_num_inputs=c_numpy.PyArray_DIMS(X)[1]

    cdef int t,k,i,count,countn,num_inputs
    cdef double scale
    cdef int offset,npics,pic
    cdef int lenx
    cdef double mean,std,min,nx
    cdef int non_pattern
    
    # TODO: do with offset, right now I just copy the first vector
    
    count=0
    countn=0
    
    set_offsets(params)
    
    for k from 0<=k<num_channels:
        p=params['pattern_input'][k]

        num_inputs=p['num_inputs']
        t=p['type']
        pattern_probability=p['pattern_probability']
        if randu()>pattern_probability:  # don't apply the pattern
            non_pattern=True
            t=0  # no pattern
        else:
            non_pattern=False  # double negative!  :)
        
            
        if t==0:  # none
            Mask=p['mask']
            mask=<double *>c_numpy.PyArray_DATA(Mask)
            for i from 0<=i < num_inputs:
                x[count]=0.0
                count=count+1
                
            if non_pattern:
                n=p['non_pattern_noise']
                apply_noise(n,&x[countn],mask,num_inputs)        
                
                
        elif t==1: # data
            pic=p['offset'][0]
            offset=p['offset'][1]
            scale=p['scale']
        
            
            Im=p['var']['im'][pic]
            im=<double *>c_numpy.PyArray_DATA(Im)

            Idx=p['idx']
            idx=<int *>c_numpy.PyArray_DATA(Idx)
            
            Mask=p['mask']
            mask=<double *>c_numpy.PyArray_DATA(Mask)
                        
            for i from 0<=i < num_inputs:
                x[count]=im[idx[i]+offset]*scale*mask[i]
                count=count+1

        elif t==2: # image
            pic=p['offset'][0]
            offset=p['offset'][1]
            scale=p['scale']

            if debug:
                print "pos",pic,offset,scale
            
            Im=p['var']['im'][pic]
            im=<double *>c_numpy.PyArray_DATA(Im)

            Idx=p['idx']
            
            if debug:
                print "Index matrix:",Idx[:10]
            idx=<int *>c_numpy.PyArray_DATA(Idx)
            
            Mask=p['mask']
            mask=<double *>c_numpy.PyArray_DATA(Mask)
                        
            for i from 0<=i < num_inputs:
#             
#                 if i<10:
#                     print "[%d] offset %d idx %d img %.4f count %d" % (i,offset,idx[i],im[idx[i]+offset],count)
            
                x[count]=im[idx[i]+offset]*scale
                count=count+1

        if not non_pattern:   # an actual pattern, even if 0
            # apply the noise
            n=params['noise_input'][k]
            apply_noise(n,&x[countn],mask,num_inputs)        
            
        countn+=num_inputs
        
    # copy the network inputs
    countn=total_num_inputs
    for k from 1<=k<num_neurons:
        for i from 0<=i<total_num_inputs:
            x[countn]=x[i]
            countn+=1
            
def sigma_prime(c_numpy.ndarray Y,int output_type,double output_bottom,double output_top):
    cdef int num_neurons,n
    cdef double *y
    
    y=<double *>c_numpy.PyArray_DATA(Y)
    num_neurons=c_numpy.PyArray_DIMS(Y)[0]

    for n from 0<= n < num_neurons:
        
        if output_type==0: # nothing
            y[n]=1.0
        elif output_type==1: # tanh sigmoid
            if y[n]<0:
                y[n]=1-y[n]*y[n]/output_bottom/output_bottom
            else:
                y[n]=1-y[n]*y[n]/output_top/output_top
        elif output_type==2: # piecewise linear
            if y[n]<output_bottom:
                y[n]=0.0
            elif y[n]>output_top:
                y[n]=0.0
            else:
                y[n]=1.0
        else:
            raise ValueError,"Incorrect output type"
            
def exponential(c_numpy.ndarray Y,double output_scale):
    cdef int num_neurons,n
    cdef double *y
    
    y=<double *>c_numpy.PyArray_DATA(Y)
    num_neurons=c_numpy.PyArray_DIMS(Y)[0]

    for n from 0<= n < num_neurons:
        y[n]=exp(y[n]/output_scale)

        
def sigmoid(c_numpy.ndarray Y,int output_type,double output_bottom,double output_top):
    
    cdef int num_neurons,n
    cdef double *y
    
    y=<double *>c_numpy.PyArray_DATA(Y)
    num_neurons=c_numpy.PyArray_DIMS(Y)[0]
    
    for n from 0<= n < num_neurons:
        
        if output_type==0: # nothing
            pass
        elif output_type==1: # tanh sigmoid
            if y[n]<0:
                y[n]=output_bottom*(2.0/(1.0+exp(-2.0*(y[n]/output_bottom)))-1.0)
            else:            
                y[n]=output_top*(2.0/(1.0+exp(-2.0*(y[n]/output_top)))-1.0)
        elif output_type==2: # piecewise linear
            if y[n]<output_bottom:
                y[n]=output_bottom
            elif y[n]>output_top:
                y[n]=output_top
        else:
            raise ValueError,"Incorrect output type"
                
def calc_output(c_numpy.ndarray Y,c_numpy.ndarray R,c_numpy.ndarray X,
                c_numpy.ndarray weights,
                int output_type,double output_bottom,double output_top,
                double weight_offset,double mean_weight_offset,int use_output_noise,
                output_noise):
                       

    cdef double *x
    cdef double *y
    cdef double *r
    cdef double *w
    
    cdef int num_inputs,num_neurons
    num_neurons=c_numpy.PyArray_DIMS(weights)[0]
    num_inputs=c_numpy.PyArray_DIMS(weights)[1]

    # get the pointers
    w=<double *>c_numpy.PyArray_DATA(weights)
    x=<double *>c_numpy.PyArray_DATA(X)
    y=<double *>c_numpy.PyArray_DATA(Y)
    r=<double *>c_numpy.PyArray_DATA(R)

    cdef int n,i,ic
    
    cdef double mean_weights
    cdef mean,std,min,nx

    ic=0
    if mean_weight_offset==0.0:
        for n from 0 <= n < num_neurons:
            y[n]=0.0
            for i from 0 <= i < num_inputs:
                y[n]=y[n]+x[ic]*(w[ic]+weight_offset)
                ic=ic+1
    else:
        for n from 0 <= n < num_neurons:
            y[n]=0.0
            mean_weights=0.0
            for i from 0 <= i < num_inputs:
                mean_weights+=w[ic+i]
            mean_weights/=num_inputs
            for i from 0 <= i < num_inputs:
                y[n]=y[n]+x[ic]*(w[ic]+weight_offset-mean_weight_offset*mean_weights)
                ic=ic+1
            
    if use_output_noise:
        
        t=output_noise['type']
        
        if t==0: # none
            pass
        elif t==1: # uniform
            mean=output_noise['mean']
            std=output_noise['std']
            for n from 0 <= n < num_neurons:
                y[n]+=(randu()-0.5)*2.0*1.732050807569*std+mean
        elif t==2: # gaussian
            mean=output_noise['mean']
            std=output_noise['std']
            min=output_noise['min']
            for n from 0 <= n < num_neurons:
                nx=randn()*std+mean
                if nx<min:
                    nx=min
                y[n]+=nx

        elif t==3: # laplace
            mean=output_noise['mean']
            std=output_noise['std']
            min=output_noise['min']
            for n from 0 <= n < num_neurons:
                if randu()>0.5:
                    nx=rande()/1.414213562373*std+mean
                else:
                    nx=-rande()/1.414213562373*std+mean
                if nx<min:
                    nx=min
                y[n]+=nx
        elif t==4: # proportional
            mean=output_noise['mean']
            std=output_noise['std']
            min=output_noise['min']
            for n from 0 <= n < num_neurons:
                nx=randn()*std
                if nx<min:
                    nx=min
                y[n]+=(nx*y[n]+mean)
        
            
    if output_type==0:  # linear
        pass
    elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
        sigmoid(Y,output_type,output_bottom,output_top)
    else:
        raise ValueError,"incorrect output type"
        

def get_output_list(int num_iterations,sim):
    
    cdef c_numpy.ndarray weights,moments
    
    params=sim['params']
    weights=sim['weights'][0]
    moments=sim['moments'][0]
    
    cdef int i,it,n,count  # loop variables


    # get the pointers
    cdef double *w
    cdef double *th

    w=<double *>c_numpy.PyArray_DATA(weights)
    th=<double *>c_numpy.PyArray_DATA(moments)
    
    cdef int num_inputs,num_neurons
    num_neurons=c_numpy.PyArray_DIMS(weights)[0]
    num_inputs=c_numpy.PyArray_DIMS(weights)[1]


    cdef int save_input
    save_input=params['save_input']

    cdef int num_layers,layer,use_lat
    num_layers=len(params['lateral'])
    layer=0
    use_lat=params['lateral'][layer]['type']  

    cdef double *L
    cdef c_numpy.ndarray var
    
    if use_lat==1: # orthogonalization
        orth_weights=params['lateral'][layer]['var']
    else:
        orth_weights=None


    cdef int output_type,use_spontaneous_modification
    cdef double output_top
    cdef int use_output_derivative
    cdef double output_bottom,sigma_o,sigma_tau,weight_offset,mean_weight_offset
    cdef double output_scale
    output_type=params['output'][layer]['type']
    output_top=params['output'][layer]['top']
    output_bottom=params['output'][layer]['bottom']
    weight_offset=params['output'][layer]['weight_offset']
    mean_weight_offset=params['output'][layer]['mean_weight_offset']
    use_output_derivative=params['output'][layer]['use_derivative']
    sigma_o=params['output'][layer]['sigma_o']
    sigma_tau=params['output'][layer]['sigma_tau']
    output_scale=params['output'][layer]['scale']

    cdef int use_output_noise
    use_output_noise=params['output'][layer]['output_noise']['type']!=0
    
    cdef int learning_rule,rule=0
    
    modification_rule=get_modification_rule(params)
    learning_rule_params=modification_rule['params']
    learning_rule=modification_rule['type']

    cdef int use_beta,linear_beta
    cdef double tau_beta,tmp_y,k_beta
    
    use_beta=0
    tau_beta=0.0
    linear_beta=0
    
    if 'tau_beta' in learning_rule_params:
        tau_beta=learning_rule_params['tau_beta']
        k_beta=learning_rule_params['k_beta']
        linear_beta=learning_rule_params['linear_beta']
        if tau_beta>0:
            use_beta=1


    if params['random_seed2']:
      init_by_int(<int> params['random_seed2'])
    else:
      init_by_entropy()


    init_params(params)

    cdef c_numpy.ndarray X,Y,R,Y_SIGMOIDED

    X=np.zeros((num_neurons,num_inputs),np.float64)    
    R=np.zeros((num_neurons,num_inputs),np.float64)    
    Y=np.zeros((num_neurons,1),np.float64)    
    Y_SIGMOIDED=np.zeros((num_neurons,1),np.float64)    
    PHI=np.ones((num_neurons,1),np.float64)    

    cdef double *x
    cdef double *y
    cdef double *r
    cdef double *beta
    cdef double *y_sigmoided
    y=<double *>c_numpy.PyArray_DATA(Y)
    x=<double *>c_numpy.PyArray_DATA(X)
    r=<double *>c_numpy.PyArray_DATA(R)
    y_sigmoided=<double *>c_numpy.PyArray_DATA(Y_SIGMOIDED)
    if use_beta:
        beta=<double *> &th[num_neurons]

    output_list=[]
    for it from 0 <= it < num_iterations:

        get_input_vector(X,params)

        if save_input:
            params['saved_input_vectors'].append(X.copy())

        # do w*x only
        calc_output(Y,R,X,weights,0,0,0,weight_offset,mean_weight_offset,
            use_output_noise,params['output'][layer]['output_noise'])
        if use_beta:
            for n from 0<=n < num_neurons:
                y[n]=y[n]-beta[n]
        
        if use_lat==0 or use_lat==1 or use_lat==2:  # no lateral connectivity, or orthog
            # apply the sigmoid
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y,output_type,output_bottom,output_top)
            else:
                raise ValueError,"incorrect output type"
        else:
            for n from 0<=n < num_neurons:
                y_sigmoided[n]=y[n]
                
            
            # apply the sigmoid on a copy
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y_SIGMOIDED,output_type,output_bottom,output_top)
            else:
                raise ValueError,"incorrect output type"
                
            # now apply the lateral connectivity
            
            apply_lateral(Y,Y_SIGMOIDED,params['lateral'][layer])
            
            # apply the sigmoid
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y,output_type,output_bottom,output_top)
            else:
                raise ValueError,"incorrect output type"
                   
        if use_output_derivative:
            for n from 0<=n < num_neurons:
                y_sigmoided[n]=y[n]
            sigma_prime(Y_SIGMOIDED,output_type,output_bottom,output_top)
        
        output_list.append(y[0])
        

    return output_list

def apply_lateral(c_numpy.ndarray Y,c_numpy.ndarray Y_SIG,lateral_params):
    
    cdef int num_neurons,n
    cdef double *y
    cdef double *ys
    cdef c_numpy.ndarray var
    
    y=<double *>c_numpy.PyArray_DATA(Y)
    ys=<double *>c_numpy.PyArray_DATA(Y_SIG)
    num_neurons=c_numpy.PyArray_DIMS(Y)[0]
    
    cdef int lateral_type=lateral_params['type']
    cdef int i,j,count
    cdef double *L
    
    cdef double y0
    
    if lateral_type==0 or lateral_type==1 or lateral_type==2:  # none, Gramm, and Symm
        for n from 0<=n<num_neurons:
            y[n]=ys[n]
    elif lateral_type==3:
        var=lateral_params['var']
        L=<double *>c_numpy.PyArray_DATA(var)
        count=0
        for i from 0<=i<num_neurons:
            for j from 0<=j<num_neurons:
                y[i]+=ys[j]*L[count]
                count+=1
    elif lateral_type==4:  # uniform, modifiable
        var=lateral_params['var']
        L=<double *>c_numpy.PyArray_DATA(var)  # of length of number of neurons
        
        # get average sigma(w*x)
        y0=0.0
        for i from 0<=i<num_neurons:
            y0+=ys[i]
        y0/=num_neurons

        for i from 0<=i<num_neurons:
            y[i]+=L[i]*y0
        
    
             
    
def train(int epoch,params,
          c_numpy.ndarray weights,
          c_numpy.ndarray moments,
          c_numpy.ndarray individual_moments,
          extra_input):

    extra={}
    

    cdef int i,it,n,count,count2  # loop variables

    cdef int use_output_noise
    # get the pointers
    cdef double *w
    cdef double *th
    cdef double *old_w
    cdef double *ind_m
    
    w=<double *>c_numpy.PyArray_DATA(weights)
    th=<double *>c_numpy.PyArray_DATA(moments)
    ind_m=<double *>c_numpy.PyArray_DATA(individual_moments)
    
    cdef int num_inputs,num_neurons,num_moments
    cdef int num_channels,num_inputs_channel
    
    num_neurons=c_numpy.PyArray_DIMS(weights)[0]
    num_inputs=c_numpy.PyArray_DIMS(weights)[1]
    num_moments=c_numpy.PyArray_DIMS(moments)[0]
    num_channels=len(params['pattern_input'])
    

    cdef int num_iterations
    num_iterations=params['iter_per_epoch']
    
    cdef int save_input
    save_input=params['save_input']
    
    cdef double eta,tau
    eta=params['eta']  # learning rate
    tau=params['tau']  # used for variance estimate

    
    cdef int num_layers,layer,use_lat
    num_layers=len(params['lateral'])
    layer=0
    use_lat=params['lateral'][layer]['type']  
    
    cdef double *L
    cdef c_numpy.ndarray var
    
    if use_lat==1: # orthogonalization
        orth_weights=params['lateral'][layer]['var']
    else:
        orth_weights=None
        
    
    
    cdef int output_type,use_spontaneous_modification
    cdef double output_top
    cdef int use_output_derivative
    cdef double output_bottom,sigma_o,sigma_tau,weight_offset,mean_weight_offset
    cdef double output_scale
    output_type=params['output'][layer]['type']
    output_top=params['output'][layer]['top']
    output_bottom=params['output'][layer]['bottom']
    weight_offset=params['output'][layer]['weight_offset']
    mean_weight_offset=params['output'][layer]['mean_weight_offset']
    use_output_derivative=params['output'][layer]['use_derivative']
    sigma_o=params['output'][layer]['sigma_o']
    sigma_tau=params['output'][layer]['sigma_tau']
    output_scale=params['output'][layer]['scale']
    
    use_output_noise=params['output'][layer]['output_noise']['type']!=0
    
    
    if sigma_tau>0.0:
        use_spontaneous_modification=True
        if extra_input:
            output_bottom=extra_input[0]
        else:
            extra_input.append(output_bottom)
    else:
        use_spontaneous_modification=False
    
    cdef int learning_rule,rule=0
    
    modification_rule=get_modification_rule(params)
    learning_rule_params=modification_rule['params']
    learning_rule=modification_rule['type']

    cdef int weight_stabilization_type
    cdef double weight_stabilization_top,weight_stabilization_bottom
    cdef double decay
    cdef double gamma
    cdef double alpha
    cdef int use_beta,linear_beta
    cdef double tau_beta,tmp_y,k_beta
    cdef double beta_scale_mean,beta_scale_std,beta_shift_mean,beta_shift_std,beta_val

    
    use_beta=0
    tau_beta=0.0
    linear_beta=1
    
    weight_stabilization_type=params['weight_stabilization'][0]['type']
    weight_stabilization_bottom=params['weight_stabilization'][0]['bottom']
    weight_stabilization_top=params['weight_stabilization'][0]['top']
    decay=params['weight_stabilization'][0]['decay']
    
    if not (weight_stabilization_type==4 or weight_stabilization_type==6):
        decay=0.0
    
    cdef double _gamma  # for Log Phi rule
    
    cdef double a,b,c,theta_o,theta_p,unified_decay,theta_L,tau_theta_L
    a=0.0
    b=0.0
    c=0.0
    theta_o=0.0
    theta_p=3.0
    if 'tau_beta' in learning_rule_params:
        tau_beta=learning_rule_params['tau_beta']
        k_beta=learning_rule_params['k_beta']
        linear_beta=learning_rule_params['linear_beta']
        if tau_beta>0:
            use_beta=1

        if 'beta_scale_mean' in learning_rule_params:
            beta_scale_mean=learning_rule_params['beta_scale_mean']
            beta_scale_std=learning_rule_params['beta_scale_std']
            beta_shift_mean=learning_rule_params['beta_shift_mean']
            beta_shift_std=learning_rule_params['beta_shift_std']
        else:
            beta_scale_mean=0.0
            beta_scale_std=0.0
            beta_shift_mean=0.0
            beta_shift_std=0.0
        
    if learning_rule==4:  # user 1
        a=learning_rule_params['a']
        b=learning_rule_params['b']
        c=learning_rule_params['c']
        theta_o=learning_rule_params['theta_o']
    
    if learning_rule==5:  # user 2
        a=learning_rule_params['a']
        b=learning_rule_params['b']
        c=learning_rule_params['c']
        theta_o=learning_rule_params['theta_o']
    
    if learning_rule==6 or learning_rule==7:  # unified 1 and 2
        theta_o=learning_rule_params['theta_o']
        theta_p=learning_rule_params['theta_p']
        unified_decay=learning_rule_params['decay']
    
    if learning_rule==8:  # modify spontaneous
        sigma_o=learning_rule_params['sigma_o']
        sigma_tau=learning_rule_params['sigma_tau']

    if learning_rule==26: # Law/Cooper BCM w/ -gamma*y^2*w
        gamma=learning_rule_params['gamma']
    elif learning_rule==27: # Law/Cooper BCM w/ -gamma*y*w
        gamma=learning_rule_params['gamma']
    else:
        gamma=0.0

    cdef double theta_L_fraction,theta_L_max,k_theta_L
    
    if learning_rule==28: # Law/Cooper BCM w/ theta_L
        theta_L=learning_rule_params['theta_L']
    else:
        theta_L=0.0

    if learning_rule==29: # Law/Cooper BCM w/ theta_L_fraction
        theta_L_fraction=learning_rule_params['theta_L_fraction']
        theta_L_max=learning_rule_params['theta_L_max']
    else:
        theta_L_fraction=0.0
        theta_L_max=100000.0
        
    if learning_rule==30: # log phi
        _gamma=learning_rule_params['gamma']
        theta_o=learning_rule_params['theta_o']

    if learning_rule==31: # BCM8292
        alpha=learning_rule_params['alpha']
    else:
        alpha=0.0
        
    if learning_rule==32:  # Law/Cooper BCM with Dynamic Lower Threshold
        tau_theta_L=learning_rule_params['tau_theta_L']
    if learning_rule==33:  # Law/Cooper BCM with Dynamic Lower Threshold 2
        tau_theta_L=learning_rule_params['tau_theta_L']
        k_theta_L=learning_rule_params['k_theta_L']
    else:
        tau_theta_L=0.0
        
    if epoch==0:
        if params['random_seed2']:
            init_by_int(params['random_seed2'])
        else:
            init_by_entropy()
            
        
        init_params(params)

    cdef c_numpy.ndarray X,Y,R,PHI,Y_SIGMOIDED,old_weights
        
    X=np.zeros((num_neurons,num_inputs),np.float64)    
    R=np.zeros((num_neurons,num_inputs),np.float64)    
    Y=np.zeros((num_neurons,1),np.float64)    
    Y_SIGMOIDED=np.zeros((num_neurons,1),np.float64)    
    PHI=np.ones((num_neurons,1),np.float64)    

    cdef double *phi
    cdef double *x
    cdef double *y
    cdef double *r
    cdef double *beta
    cdef double *y_sigmoided
    cdef double *avg8292
    cdef double *theta_L_dynamic
    phi=<double *>c_numpy.PyArray_DATA(PHI)
    y=<double *>c_numpy.PyArray_DATA(Y)
    x=<double *>c_numpy.PyArray_DATA(X)
    r=<double *>c_numpy.PyArray_DATA(R)
    y_sigmoided=<double *>c_numpy.PyArray_DATA(Y_SIGMOIDED)
    
    cdef double sum,tmp1,tmp2,sum2
    
    if use_beta:
        beta=<double *> &th[num_neurons]

        if learning_rule==31:        
            avg8292=<double *> &th[2*num_neurons]
        elif learning_rule==32 or learning_rule==33: # Law/Cooper BCM with Dynamic Lower Threshold
            theta_L_dynamic=<double *> &th[2*num_neurons]
            for n from 0<=n < num_neurons:
                theta_L_dynamic[n]=0.0
                    
    else:
        if learning_rule==31:        
            avg8292=<double *> &th[num_neurons]
        elif learning_rule==32 or learning_rule==33: # Law/Cooper BCM with Dynamic Lower Threshold
            theta_L_dynamic=<double *> &th[num_neurons]
            for n from 0<=n < num_neurons:
                theta_L_dynamic[n]=0.0

    for it from 0 <= it < num_iterations:
        if weight_stabilization_type==5: # saturation w/o zero cross
            old_weights=weights.copy()
            old_w=<double *>c_numpy.PyArray_DATA(old_weights)

        get_input_vector(X,params)
        
        if debug:
            print "X",X.ravel()[:50]
        
        if save_input:
            params['saved_input_vectors'].append(X.copy())

        # do w*x only
        calc_output(Y,R,X,weights,0,0,0,weight_offset,mean_weight_offset,
            use_output_noise,params['output'][layer]['output_noise'])
        
        
        
        if use_beta:
            if linear_beta:
                for n from 0<=n < num_neurons:
                    # calc beta with w*x only
                    beta_val=k_beta*y[n]
                    if beta_scale_std>0:
                        beta_val*=randn()*beta_scale_std+beta_scale_mean
                        # beta_val*=((randu()-0.5)*2.0*1.732050807569*beta_scale_std+beta_scale_mean)
                    if beta_shift_std>0:
                        beta_val+=(randn()*beta_shift_std+beta_shift_mean)
                                        
                    beta[n]=beta[n]+(beta_val-beta[n])/tau_beta
                    
                    y[n]=y[n]-beta[n]
            else:
                for n from 0<=n < num_neurons:
                    y[n]=y[n]-beta[n]
        if debug:
            print "Y",Y.ravel()

        if use_lat==0 or use_lat==1 or use_lat==2:  # no lateral connectivity, or orthog
            # apply the sigmoid
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y,output_type,output_bottom,output_top)
            elif (output_type==3): # exponential
                exponential(Y,output_scale)
            else:
                raise ValueError,"incorrect output type"
        else:
            for n from 0<=n < num_neurons:
                y_sigmoided[n]=y[n]
                
            
            # apply the sigmoid on a copy
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y_SIGMOIDED,output_type,output_bottom,output_top)
            else:
                raise ValueError,"incorrect output type"
                
            # now apply the lateral connectivity
            
            apply_lateral(Y,Y_SIGMOIDED,params['lateral'][layer])
            
            # apply the sigmoid
            if output_type==0:  # linear
                pass
            elif (output_type==1) or (output_type==2): # sigmoid or piecewise linear
                sigmoid(Y,output_type,output_bottom,output_top)
            else:
                raise ValueError,"incorrect output type"
                   
        if use_output_derivative:
            for n from 0<=n < num_neurons:
                y_sigmoided[n]=y[n]
            sigma_prime(Y_SIGMOIDED,output_type,output_bottom,output_top)
            
        if use_beta and not linear_beta:
            for n from 0<=n < num_neurons:
                # calc beta with y, after sigmoids, etc...
                beta_val=k_beta*y[n]
                if beta_scale_std>0:
                    beta_val*=randn()*beta_scale_std+beta_scale_mean
                    # beta_val*=((randu()-0.5)*2.0*1.732050807569*beta_scale_std+beta_scale_mean)
                if beta_shift_std>0:
                    beta_val+=(randn()*beta_shift_std+beta_shift_mean)

                beta[n]=beta[n]+(beta_val-beta[n])/tau_beta
        
        if debug:    
            print "Y sig",Y.ravel()
            
        if learning_rule==0:  # nothing
            pass
        elif learning_rule==1: # bcm
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*(y[n]-th[n])
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                if debug:    
                    print "phi",phi[n]
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    
                    if debug:
                        if i<50:
                            print w[count],x[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                
                if debug:
                    print "th",th[n]
            
                
                blah['y'].append(y[n])
                blah['phi'].append(phi[n])                
                
        elif learning_rule==2: # law and cooper bcm
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*(y[n]-th[n])/th[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==26: # law and cooper bcm with -gamma*y^2 w
                            #, kinda-like oja
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*(y[n]-th[n])/th[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]-eta*gamma*y[n]*y[n]*w[count]
                    count=count+1
        elif learning_rule==27: # law and cooper bcm with -gamma*y w
                            #, kinda-like oja
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*(y[n]-th[n])/th[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]-eta*gamma*y[n]*w[count]
                    count=count+1
                
        elif learning_rule==28: # law and cooper bcm with theta_L
            count=0
            for n from 0<=n < num_neurons:
                if y[n]<theta_L:
                    y[n]=theta_L

                phi[n]=eta*(y[n]-theta_L)*(y[n]-th[n])/th[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                if th[n]<theta_L:
                    th[n]=theta_L
                    
        elif learning_rule==29: # law and cooper bcm with theta_L_fraction
            count=0
            for n from 0<=n < num_neurons:
                theta_L=theta_L_fraction*th[n]
                if theta_L>theta_L_max:
                    theta_L=theta_L_max

                if y[n]<theta_L:
                    y[n]=theta_L
                    
                phi[n]=eta*(y[n]-theta_L)*(y[n]-th[n])/th[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                if th[n]<theta_L:
                    th[n]=theta_L
                
        elif learning_rule==3: # hebb
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==4: # user1  
            #  start from equation 14, replace Y with a+bV+c*V**2, where V is the
            #postsynaptic activity
            #   S is sigmoid of input
            

            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    tmp1=a+b*y[n]+c*y[n]*y[n]
                    
                    w[count]=w[count]+eta*( (theta_o/th[n])**3 * 
                                        (x[count]*tmp1)**2 *
                                        (x[count]*tmp1-th[n])
                                      
                                        -(theta_o/th[n])*
                                          (x[count]*tmp1)*w[count])-eta*decay*w[count]
                    
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==5: # user2: hebb with scaling
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+(phi[n]*x[count]-eta*decay*w[count])/th[n]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==6: # unified 1
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+ (
                       eta*(theta_o**theta_p/th[n]**theta_p)*x[count]*
                               (x[count]*y[n])**2*(x[count]*y[n]-th[n])-
                       unified_decay*eta*theta_o/th[n]*x[count]**2*y[n]*w[count]
                    )
                    
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
            
            
            
        elif learning_rule==7: # unified 2
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+ (
                       eta*(theta_o**theta_p/th[n]**theta_p)*x[count]*
                               (x[count]*y[n])**2*(y[n]-th[n])-
                       unified_decay*eta*theta_o/th[n]*x[count]*y[n]*w[count]
                    )
                    
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                
            
        elif learning_rule>=9 and learning_rule<(9+12): # different rules
            rule=learning_rule-9+1
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"

                
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    if rule==1:  # traditional BCM
                        w[count]=w[count]+eta*y[n]*(y[n]-th[n])*x[count]
                    elif rule==2:
                        w[count]=w[count]+eta*y[n]*y[n]*(y[n]-th[n])*x[count]
                    elif rule==3:
                        w[count]=w[count]+eta*y[n]*y[n]*(y[n]-th[n])
                    elif rule==4:
                        w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(x[count]*y[n]-th[n])
                    elif rule==5:
                        w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(x[count]*y[n]-th[n])*x[count]
                    elif rule==6:
                        w[count]=w[count]+eta*(x[count]*y[n])*(y[n]-th[n])*x[count]
                    elif rule==7:
                        w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(y[n]-th[n])*x[count]
                    elif rule==8:
                        w[count]=w[count]+eta*(y[n]*y[n])*(y[n]-th[n])*x[count]*x[count]
                    elif rule==9:
                        w[count]=w[count]+eta*(x[count]*y[n])*(y[n]-th[n])*x[count]*x[count]
                    elif rule==10:
                        w[count]=w[count]+eta*(x[count]*y[n])*(y[n]*x[count]-th[n])*x[count]
                    elif rule==11:
                        w[count]=w[count]+eta*y[n]*(y[n]-th[n])*x[count]*x[count]
                    elif rule==12:
                        w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(y[n]-th[n])*x[count]*x[count]*x[count]
                    
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
            
            
        elif learning_rule==21:  # individual thresholds
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(y[n]*x[count]-ind_m[count])*x[count]
                    count=count+1
                    
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    ind_m[count]=ind_m[count]+(y[n]*y[n]*x[count]-ind_m[count])/tau
                    count=count+1
        elif learning_rule==22:
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(y[n]-th[n])*x[count]/th[n]
            
                    count=count+1
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==23:
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+eta*(x[count]*y[n]*x[count]*y[n])*(y[n]-th[n])*x[count]/th[n]/th[n]
            
                    count=count+1
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau

        elif learning_rule==24:
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+eta*y[n]*(y[n]-th[n])*x[count]*x[count]/th[n]
            
                    count=count+1
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
        elif learning_rule==25:
            if use_output_derivative: # apply sigma_prime - not implemented
                raise ValueError,"sigma prime not implemented"
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+eta*y[n]*(y[n]-th[n])*x[count]*x[count]/th[n]/th[n]
            
                    count=count+1
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau

        elif learning_rule==30: # log phi - only makes sense for positive y
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*log(y[n]/th[n])
                if use_output_derivative: # apply sigma_prime
                    raise ValueError,"Log phi no output derivative"
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*pow(y[n]/theta_o,_gamma)-th[n])/tau
        elif learning_rule==31: # BCM8292 dw/dt=eta*y*(y-theta) x, theta ~ E[y^(1+alpha)]^(2-alpha)
            # alpha=0 = BCM82, alpha=1 = BCM92
            count=0
            for n from 0<=n < num_neurons:
                phi[n]=eta*y[n]*(y[n]-th[n])
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                # need a second variable to be the average
                avg8292[n]=avg8292[n]+(pow(y[n],1+alpha)-avg8292[n])/tau
                th[n]=pow(avg8292[n],2-alpha)
                
        elif learning_rule==32: # Law/Cooper BCM with Dynamic Lower Threshold'
            count=0
            for n from 0<=n < num_neurons:
                if y[n]<theta_L_dynamic[n]:
                    phi[n]=0.0
                else:
                    phi[n]=eta*(y[n]-theta_L_dynamic[n])*(y[n]-th[n])/th[n]
                    
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                theta_L_dynamic[n]=theta_L_dynamic[n]+(y[n]-theta_L_dynamic[n])/tau_theta_L
        elif learning_rule==33: # Law/Cooper BCM with Dynamic Lower Threshold'
            count=0
            for n from 0<=n < num_neurons:
                if y[n]<theta_L_dynamic[n]:
                    phi[n]=0.0
                else:
                    phi[n]=eta*(y[n]-theta_L_dynamic[n])*(y[n]-th[n])/th[n]
                    
                if use_output_derivative: # apply sigma_prime
                    phi[n]*=y_sigmoided[n]
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]+phi[n]*x[count]-eta*decay*w[count]
                    count=count+1
                    
                th[n]=th[n]+(y[n]*y[n]-th[n])/tau
                theta_L_dynamic[n]=theta_L_dynamic[n]+(y[n]*y[n]*k_theta_L-theta_L_dynamic[n])/tau_theta_L
                
        else:
            raise ValueError,"Unknown learning rule: "+str(learning_rule)
        
        if use_lat==4:  # uniform, modify lateral 
            var=params['lateral'][layer]['var']
            L=<double *>c_numpy.PyArray_DATA(var)  # of length of number of neurons
            
            # get average sigma(w*x)
            y0=0.0
            for n from 0<=n<num_neurons:
                y0+=y_sigmoided[n]
            y0/=num_neurons

            for n from 0<=n<num_neurons:
                L[n]+=eta*(-phi[n]*y0-L[n])
        
        if use_spontaneous_modification:
            output_bottom=-output_bottom
            output_bottom=output_bottom+(y[0]*y[0]-output_bottom/sigma_o)/sigma_tau
            output_bottom=-output_bottom
        
        
                
        if weight_stabilization_type==0: # nothing
            pass
        elif weight_stabilization_type==1: # oja
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    w[count]=w[count]-phi[n]*y[n]*w[count]
                    count=count+1
        elif weight_stabilization_type==2: # strict
            count=0
            for n from 0<=n < num_neurons:
                sum=0.0
                for i from 0<=i<num_inputs:
                    sum=sum+w[count]*w[count]
                    count=count+1
                    
                count=count-num_inputs
                sum=sqrt(sum)
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]/sum
                    count=count+1
        elif weight_stabilization_type==7: # all positive normalization
            count=0
            for n from 0<=n < num_neurons:
                sum=0.0
                for i from 0<=i<num_inputs:
                    if w[count]<0.0:
                        w[count]=0.0
                
                    sum=sum+w[count]*w[count]
                    count=count+1
                    
                count=count-num_inputs
                sum=sqrt(sum)
                
                for i from 0<=i<num_inputs:
                    w[count]=w[count]/sum
                    count=count+1
            
            
            
        elif weight_stabilization_type==8: # saturated gerstner normalization
            # N=len(c.w)
            # n0=norm(c.w)
            # n_on=norm(c.w[:N/2])
            # n_off=norm(c.w[N/2:])
            # 
            # c.w[:N/2]=c.w[:N/2]/n_on*n0/sqrt(2)
            # c.w[N/2:]=c.w[N/2:]/n_off*n0/sqrt(2)

            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    if w[count]>weight_stabilization_top:
                        w[count]=weight_stabilization_top
                    elif w[count]<weight_stabilization_bottom:
                        w[count]=weight_stabilization_bottom
                    count=count+1

            # i.e. find the norm of all weights, and make the individual channels have that norm
            count=0
            for n from 0<=n < num_neurons:
                sum2=0.0
                for i from 0<=i<num_inputs:
                
                    sum2=sum2+w[count]*w[count]
                    count=count+1
                    
                count=count-num_inputs
                sum2=sqrt(sum2)

                
                # normalize all the channels to that one
                for k from 0 <= k < num_channels:
                    num_inputs_channel=params['pattern_input'][k]['num_inputs']
                    sum=0.0
                    count2=count
                    for i from 0<=i<num_inputs_channel:                    
                        sum=sum+w[count]*w[count]
                        count=count+1
                        
                    count=count2
                    sum=sqrt(sum)
                    
                    for i from 0<=i<num_inputs_channel:
                        w[count]=w[count]/sum*sum2/sqrt(num_channels)
                        count=count+1

            
            
        elif (weight_stabilization_type==3 or weight_stabilization_type==6): # saturation
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    if w[count]>weight_stabilization_top:
                        w[count]=weight_stabilization_top
                    elif w[count]<weight_stabilization_bottom:
                        w[count]=weight_stabilization_bottom
                    count=count+1
        elif weight_stabilization_type==4: # weight decay
             pass  
        elif weight_stabilization_type==5: # saturation w/o zero cross
            count=0
            for n from 0<=n < num_neurons:
                for i from 0<=i<num_inputs:
                    if w[count]*old_w[count]<0:  # opposite sign
                        w[count]=old_w[count]
                
                    if w[count]>weight_stabilization_top:
                        w[count]=weight_stabilization_top
                    elif w[count]<weight_stabilization_bottom:
                        w[count]=weight_stabilization_bottom
                    count=count+1
        #elif weight_stabilization_type==6: # weight decay with saturation
        #     pass # done above
        else: 
            raise ValueError,"unknown weight stabilization type: " + str(weight_stabilization_type)
           
           
    cdef double *w2
    cdef c_numpy.ndarray W2arr
    
    if use_lat==1:  # orthog 
        W2=matrix(weights)
        
        for n from 1<=n<num_neurons:  # "1" is on purpose here: from second neuron on
            Wp=array(W2[0:n,:])
            norms=np.sqrt(np.sum(Wp**2,axis=1))
            norms.shape=(n,1)
            Wp/=norms  # normalize
            Wp=matrix(Wp)
            W2[n,:]-= W2[n,:]*Wp.T*Wp

        if orth_weights:
            for Wp in orth_weights:
                norms=np.sqrt(np.sum(Wp**2,axis=1))
                norms.shape=(Wp.shape[0],1)
            
                Wp/=norms  # normalize
                Wp=matrix(Wp)
                W2-=W2*Wp.T*Wp
            

        count=0
        W2arr=W2
        w2=<double *>c_numpy.PyArray_DATA(W2arr)
        for n from 0<=n < num_neurons:
            for i from 0<=i<num_inputs:
                w[count]=w2[count]
                count=count+1


    elif use_lat==2: # symm
        pass
    
    if use_lat==4:
        extra['L']=var=params['lateral'][layer]['var'][:]
           
    extra['mean weights']=np.mean(weights)
    extra['y0']=y[0]
    
    if use_spontaneous_modification:
        extra['output_bottom']=output_bottom
        extra_input[0]=output_bottom
    
    
    extra['blah']=blah
    return extra
