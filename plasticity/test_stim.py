import numpy
from train import *

from numpy import cos,sin,arctan2
pi=numpy.pi

def prod(l):

    if l:
        p=1

        for v in l:
            p=p*v

        return p
    else:
        return None


    
    
    

def test_OR_single(params,weights):
    

    num_channels=len(params['pattern_input'])
    
    rf_diameter=numpy.sqrt(params['pattern_input'][0]['num_inputs'])
    
    layer=0
    test_stim=params['test_stimulus'][layer]
    
    numang=test_stim['numang']
    k=test_stim['k']
    
    num_inputs=0
    for p in params['pattern_input']:
        num_inputs=num_inputs+p['num_inputs']
    num_neurons=prod(params['num_neurons'])

    
    inputs_per_channel=params['pattern_input'][0]['num_inputs']
    mask=get_circle_mask(inputs_per_channel).ravel()
    
    # each angle tested: the +pi/2 is the difference between having the axis
    # along which the sine value changes be 0 degrees, or a "bar" at zero
    # degrees with high values of the sign grating up, and low values down
    

    theta=numpy.linspace(0.0,pi,numang)+pi/2
    x=numpy.linspace(0.0,pi,numang)*180.0/pi
    
    i,j= numpy.mgrid[-rf_diameter//2:rf_diameter//2,
                            -rf_diameter//2:rf_diameter//2]
    i=i+1
    j=j+1
    
    i=i.ravel()
    j=j.ravel()
    
    sine_gratings=[]
    cosine_gratings=[]
    
    for t in theta:
        kx=k*cos(t)
        ky=k*sin(t)
        
        
        sine_gratings.append(sin(kx*i+ky*j))   # sin grating input (small amp)
        cosine_gratings.append(cos(kx*i+ky*j))   # cos grating input (small amp)
    

    response_vars=[]
    for jn in range(num_neurons):
        count=0
        for p in params['pattern_input']:
    
            
            N=p['num_inputs']
        
            weights_1channel_1neuron=weights[0][jn,count:count+N]*mask

            y=[]
            for ds,dc in zip(sine_gratings,cosine_gratings):
            
                cs=(weights_1channel_1neuron*ds).sum() # response to sin/cos grating input
                cc=(weights_1channel_1neuron*dc).sum()
                
                phi=arctan2(cc,cs)  # phase to give max response
                
                c=cs*cos(phi)+cc*sin(phi)     # max response
            
                y.append(c)
                
            val=(max(y),x,y)
      
            response_vars.append(val)
            
            count=count+N;
            
            
    return response_vars



def test_OR_single_gratings(params):


    num_channels=len(params['pattern_input'])

    rf_diameter=numpy.sqrt(params['pattern_input'][0]['num_inputs'])

    layer=0
    test_stim=params['test_stimulus'][layer]

    numang=test_stim['numang']
    k=test_stim['k']

    num_inputs=0
    for p in params['pattern_input']:
        num_inputs=num_inputs+p['num_inputs']
    num_neurons=prod(params['num_neurons'])


    inputs_per_channel=params['pattern_input'][0]['num_inputs']
    mask=get_circle_mask(inputs_per_channel).ravel()

    # each angle tested: the +pi/2 is the difference between having the axis
    # along which the sine value changes be 0 degrees, or a "bar" at zero
    # degrees with high values of the sign grating up, and low values down


    theta=numpy.linspace(0.0,pi,numang)+pi/2
    x=numpy.linspace(0.0,pi,numang)*180.0/pi

    i,j= numpy.mgrid[-rf_diameter//2:rf_diameter//2,
                            -rf_diameter//2:rf_diameter//2]
    i=i+1
    j=j+1

    i=i.ravel()
    j=j.ravel()

    sine_gratings=[]
    cosine_gratings=[]

    for t in theta:
        kx=k*cos(t)
        ky=k*sin(t)


        sine_gratings.append(sin(kx*i+ky*j))   # sin grating input (small amp)
        cosine_gratings.append(cos(kx*i+ky*j))   # cos grating input (small amp)

    return sine_gratings,cosine_gratings
