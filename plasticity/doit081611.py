from utils import *

def get_weight_modification_orig(type=1):

    params={}

    params['types']=['None','BCM','Law/Cooper BCM','Hebb','User1','User2',
                    'Unified Presyn','Unified 2','Modified Spontaneous',
                    ]
    params['types'].extend(['Rule #%d' % i for i in range(1,13)])
    params['types'].append('Individual Thresholds #1')
    
    params['images']=[None,'bcm','lawcooper','hebb',None,None,
                      'unified1','unified2',None,
                      ]
    params['images'].extend([None]*12)
    params['images'].append(None)
    
    params['params']=[{},
                      {'tau_beta':0},
                      {'tau_beta':0},
                      {},
                      {'theta_o':3,'a':1,'b':0,'c':0},
                      {'theta_o':3,'a':1,'b':0,'c':0},
                      {'theta_o':1,'theta_p':3,'decay':1},
                      {'theta_o':1,'theta_p':3,'decay':1},
                      {'sigma_o':1,'sigma_tau':0},
                      ]
    params['params'].extend([{'tau_beta':0}]*12)
    params['params'].append({})

    return params
    
p1=get_weight_modification()
p2=get_weight_modification_orig()

for i,t in enumerate(p2['types']):
    print t,'==',p1['rules'][i]
    
for i,t in enumerate(p2['types']):
    print t,'==',i
    

    
params=default_params()
print "num moments:",get_num_moments(params)
