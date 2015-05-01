#!/usr/bin/env python

from utils import *
import os
import sys
import zpickle
import time
import numpy
from copy import deepcopy
import pdb
import pylab

debugit=pdb.set_trace

from train import *
from test_stim import *




def sec2str(tm):
    
    frac=tm-int(tm)
    tm=int(tm)
    
    s=''
    sc=tm % 60
    tm=tm//60
    
    mn=tm % 60
    tm=tm//60
    
    hr=tm % 24
    tm=tm//24
    dy=tm

    if (dy>0):
        s=s+"%d d, " % dy

    if (hr>0):
        s=s+"%d h, " % hr

    if (mn>0):
        s=s+"%d m, " % mn


    s=s+"%.2f s" % (sc+frac)

    return s
    

def status(txt,parent=None):

    if not parent:
        print txt
        sys.stdout.flush()
    else:
        parent.SetStatusText(txt)

def prod(l):
    
    if l:
        p=1
        
        for v in l:
            p=p*v
            
        return p
    else:
        return None


    
def subplot(*args):
    
    if len(args)==1:
        return pylab.subplot(args[0])
        
    elif len(args)==3:
        return pylab.subplot(args[0],args[1],args[2])
        
    elif len(args)==4:

        r=args[2]
        c=args[3]
        
        return pylab.subplot(args[0],args[1],c+(r-1)*args[1]);
        
        
    else:
        raise ValueError,"invalid number of arguments"
    
    
def Plot(sim):
    gray=pylab.cm.gray
    pylab.ion()
    
    try:
        if not sim['params']['display']:
            return
    except TypeError:  # sent a string
        sim=zpickle.load(sim)

        
    try:
        if sim['params']['display_module']:
            pass
    except:
        sim['params']['display_module']=False
        
    if sim['params']['display_module']:
        try:
            module=__import__(sim['params']['display_module'],fromlist=['UserPlot'])
        except ImportError:
            sim['params']['display']=False
            print "Error","Error in Import: %s.  Turning display off.  %s" % (
                                sim['params']['display_module'],
                                sys.exc_info())
            return
        
        try:
            module.UserPlot(None,sim)
            pylab.draw()
            return
        except ValueError:
            sim['params']['display']=False
            print "Error in display.  Turning display off"
            return
    
    try:
    
        im=weights2image(sim['params'],sim['weights'])
        ax=pylab.subplot(221)
        pylab.pcolor(im,cmap=gray)
        ax.set_axis_bgcolor('k')
        pylab.axis('equal')
        
        num_moments=sim['moments_mat'].shape[0]

        
        ax=pylab.subplot(222)
        ax.hold(False)
        if num_moments==1:
            num_neurons=sim['moments_mat'].shape[1]
            for k in range(num_neurons):
                pylab.plot(sim['t_mat'],sim['moments_mat'][0,k,:],'-o')
                ax.hold(True)
        elif num_moments==2:
            num_neurons=sim['moments_mat'].shape[1]
            for k in range(num_neurons):
                pylab.plot(sim['t_mat'],sim['moments_mat'][0,k,:],'b-o')
                ax2=pylab.twinx(ax)
                pylab.plot(sim['t_mat'],sim['moments_mat'][1,k,:],'g-o')
                ax2.yaxis.tick_right()

        else:
            num_neurons=sim['moments_mat'].shape[1]
            for k in range(num_neurons):
                for i in range(num_moments):
                    pylab.plot(sim['t_mat'],sim['moments_mat'][i,k,:],'-o')
                    ax.hold(True)
        
        
    
        pylab.subplot(223)
        pylab.hold(False)
        response_mat=sim['response_mat']
        response_var_list=sim['response_var_list']
        
        
        styles=['b-','g-','r-','k-']
        ls=len(styles)
        for i,r in enumerate(response_var_list[-1]):
            x=r[1]
            y=r[2]
        
            pylab.plot(x,y,styles[i % ls]+"o")
            pylab.hold(True)
    
        pylab.subplot(224)
        pylab.hold(False)
        for i,r in enumerate(response_mat):
            pylab.plot(r,styles[i % ls])
            pylab.hold(True)
    
    
        pylab.draw()


    except ValueError:
        sim['params']['display']=False
        print "Error in display.  Turning display off"
        return
            
def fix_images_directories(params,parent):
    
    parts=os.path.split(__file__)
    
    for p in params['pattern_input']:
        if p['filename']:
            if not os.path.exists(p['filename']):
                filename=parts[0]+"/"+p['filename']
                if os.path.exists(filename):
                    p['filename']=filename
                else:
                    if parent is None:
                        raise ValueError,"File %s doesn't exist." % filename
                    else:
                        import warnings
                        warnings.warn("File %s doesn't exist.  Replacing with None" % filename)
                        
                        p['filename']=None
    

def hist(x,nbins=100):

    vals,bin_edges=pylab.histogram(x,nbins)
    bins=(bin_edges[1:]+bin_edges[:-1])/2
    dx=bins[1]-bins[0]
    vals=1.0*vals/sum(vals)/dx

    return bins,vals
    
def mark(vals,style='r-',direction='vertical',**kwargs):

    ax=pylab.gca()
    if direction.startswith('v'):
        
        yl=ax.get_ylim()
        for val in vals:
            pylab.plot([val,val],yl,style,**kwargs)
        
        ax.set_ylim(yl)
    elif direction.startswith('b'): # both
        xl=ax.get_xlim()
        for val in vals:
            pylab.plot(xl,[val,val],style,**kwargs)
        ax.set_xlim(xl)

        yl=ax.get_ylim()
        for val in vals:
            pylab.plot([val,val],yl,style,**kwargs)
        
        ax.set_ylim(yl)
    else: # horizontal
        xl=ax.get_xlim()
        for val in vals:
            pylab.plot(xl,[val,val],style,**kwargs)
        ax.set_xlim(xl)
    
    pylab.draw()

def pearson_correlation(x,y):
    n=len(x)
    r=(n*(x*y).sum()-x.sum()*y.sum())/numpy.sqrt( (n*(x*x).sum()-x.sum()**2)*(n*(y*y).sum()-y.sum()**2)   )
    return r

def plot_input_distribution(sim_or_params,xlabels=None,bins=50,use_log=False):
    if 'params' in sim_or_params:
        params=sim_or_params['params']
    else:
        params=sim_or_params

    fix_images_directories(params,None)    
    init_params(params)
    colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    number_of_channels=len(params['pattern_input'])
    pylab.figure(figsize=(14,3))
    h=[]
    for channel in range(number_of_channels):
        #subplot(1,number_of_channels,channel+1)

        var=params['pattern_input'][channel]['var']['im']
        x=[]
        for im in var:
            x.extend(im.ravel())
        
        x=pylab.array(x)
        b,n=hist(x,bins)
        n=n+.01
        h.append(pylab.plot(b,n,colors[channel]+'-o')[0])
    
        if use_log:
            pylab.gca().set_yscale('log')
            
            
        mark([x.max(),x.min()],colors[channel]+'--',linewidth=2)
        mark([x.mean()],colors[channel]+':')
        
        
    if number_of_channels==2:
        var0=params['pattern_input'][0]['var']['im']
        var1=params['pattern_input'][1]['var']['im']
        v0=numpy.concatenate(var0).ravel()
        v1=numpy.concatenate(var1).ravel()
        r=pearson_correlation(v0,v1)        
        pylab.title('Pearson r=%.3f' % r)

                           
    pylab.legend(h,xlabels)
    pylab.draw()
    
        
def run_sim_client(params=None,url='http://localhost:4242'):
    
    from xmlrpclib import ServerProxy
    import pickle
    
    server=ServerProxy('http://localhost:4242')
    
    if not params:
        params=default_params()
        
    params_bytes=pickle.dumps(params,0)
    
    if params['load_sim_file']:
        fid=open(params['load_sim_file'],'rb')
        bytes=fid.read()
        fid.close()
        
        lf_bytes=pickle.dumps(bytes,0)
    else:
        lf_bytes=''
    
    sim_bytes=server.run_sim_server(params_bytes,lf_bytes)
    
    sim=pickle.loads(sim_bytes)
    
    print 'Save: %s' % params['save_sim_file']
    zpickle.save(sim,params['save_sim_file'])
    
    return sim
    
    
def run_sim_server(params_bytes,lf_bytes):
    import warnings
    import os
    import pickle

    params=pickle.loads(params_bytes)

    params['display']=False
    
    # turn off security warning on tmpnam.  why is it here?
    warnings.filterwarnings('ignore')    
    sfname=os.tempnam()
    lfname=os.tempnam()
    warnings.resetwarnings()
    
    
    sfname=sfname+"_plasticity.dat"
    params['save_sim_file']=sfname
    
    if lf_bytes:
        lfname=lfname+"_plasticity.dat"
        bytes=pickle.loads(lf_bytes)
        fid.open(lfname,'wb')
        fid.write(bytes)
        fid.close()
        params['load_sim_file']=lfname
    
    sim=run_sim(params)

    sim_bytes=pickle.dumps(sim,0)

    if os.path.exists(sfname):
        os.remove(sfname)
        
    if os.path.exists(lfname):
        os.remove(lfname)
    
    return sim_bytes
    
    
def run_sim(params=None,parent=None):
    
    if not params:
        params=default_params()
    elif isinstance(params,basestring):
        fname=params
        d=zpickle.load(fname)
    
        params=d['params']
        
    
    if parent:
        save_sim_file=params['tmpfile']
        params['display']=1
    else:
        save_sim_file=params['save_sim_file']
        if params['load_sim_file']==params['tmpfile']:
            params['load_sim_file']=''
            
            
    if not save_sim_file is None and not save_sim_file:
        save_sim_file='sims/untitled.dat'

        
    # Deal the random number seed here
    
    if params['random_seed']=='clock':
        numpy.random.seed(None)
    else:
        numpy.random.seed(params['random_seed'])
        
    params['actual_random_seed']=numpy.random.get_state()
    params['random_seed2']=int(round(numpy.random.rand()*1e6))
    
    start_time=time.time()
    end_time=None
    sim_time=None
    
    num_channels=len(params['pattern_input'])
    
    num_moments=get_num_moments(params)
    
    
    layer=0
    test_stimulus=params['test_stimulus'][layer]['type']
    
    total_num_inputs=0
    for p in params['pattern_input']:
        total_num_inputs=total_num_inputs+p['num_inputs']
        

    num_neurons=prod(params['num_neurons'])
    
    if params['load_sim_file']:
        
        d=zpickle.load(params['load_sim_file'])
        load_sim_params=d['params']
        
        weights=d['weights']
        moments=d['moments']
        individual_moments=d['individual_moments']
        
        initial_weights=d['weights']
        initial_moments=d['moments']
        initial_individual_moments=d['individual_moments']
        t_mat=None
        
        if params['continue']:
            t_mat=d['t_mat']
            moments_mat=d['moments_mat']
            individual_moments_mat=d['individual_moments_mat']
            response_mat=d['response_mat']
            weights_mat=d['weights_mat']
            
            if not t_mat:
                moments_mat=None
                individual_moments_mat=None
                response_mat=None
        else:
            params['initial_weights']=deepcopy(weights)
            params['initial_moments']=deepcopy(moments)
            params['initial_individual_moments']=deepcopy(individual_moments)

            initial_weights=params['initial_weights']
            initial_moments=params['initial_moments']
            initial_individual_moments=params['initial_individual_moments']
            
    else:
        params['continue']=0
        
        full_mask=get_full_mask(params)
        
        if not params['initial_weights']:
            params['initial_weights']=[numpy.asarray(numpy.random.rand(num_neurons,total_num_inputs)*
                (params['initial_weight_range'][1]-params['initial_weight_range'][0])+
                 params['initial_weight_range'][0],numpy.float64)]

            # I love broadcasting! full_mask has a length of the number of inputs
            params['initial_weights'][layer]=params['initial_weights'][layer]*full_mask
            
        initial_weights=params['initial_weights']
        
        if not params['initial_moments']:
            params['initial_moments']=[
                numpy.asarray(
                    numpy.random.rand(num_moments,num_neurons)*
                    (params['initial_moment_range'][1]-params['initial_moment_range'][0])
                    +params['initial_moment_range'][0],numpy.float64)]

            # same size as the weights - make into a list if you need to 
            # have more of these
            params['initial_individual_moments']=[
                numpy.asarray(
                    numpy.random.rand(num_neurons,total_num_inputs)*
                    (params['initial_moment_range'][1]-params['initial_moment_range'][0])
                    +params['initial_moment_range'][0],numpy.float64)]

        initial_moments=params['initial_moments']
        initial_individual_moments=params['initial_individual_moments']

        moments_mat=numpy.dstack( (initial_moments[0],) )
        
        t_mat=None
    
    
    if not t_mat:  # not loaded from file
        
        t_mat=[0]
        start_epoch=1
        moments_mat=numpy.dstack( (initial_moments[0],) )
        
        if params['keep_every_epoch']:
            weights_mat=[initial_weights]
            individual_moments_mat=[initial_individual_moments]
        else:
            weights_mat=[]
            individual_moments_mat=[]

        response_mat=[]
        response_var=[]
        
        
        test_stimulus_type=params['test_stimulus'][layer]['type']
        if test_stimulus_type==1: # test OR single
 
            response_var=test_OR_single(params,initial_weights)
            if not response_var:
                params['test_stimulus'][layer]['type']=0
            else:
                for r in response_var:
                    response_mat.append([r[0]])
        
        
    else:
        start_epoch=len(t_mat)
        test_stimulus_type=params['test_stimulus'][layer]['type']
        response_var=[]
        if test_stimulus_type==1: # test OR single
            
            response_var=test_OR_single(params,initial_weights)
            if not response_var:
                params['test_stimulus'][layer]['type']=0
            else:
                for r,m in zip(response_var,response_mat):
                    m.append(r[0])
    

        
    weights=deepcopy(initial_weights)
    moments=deepcopy(initial_moments)
    individual_moments=deepcopy(initial_individual_moments)
    
    
    response_var_list=[response_var]

    extra_mat=[]
    
    sim={'params':params,
            'weights':weights,
            'moments':moments,
            'individual_moments':individual_moments,
            'moments_mat':moments_mat,
            'individual_moments_mat':individual_moments_mat,
            'weights_mat':weights_mat,
            'response_mat':response_mat,
            'response_var_list':response_var_list,
            'initial_weights':initial_weights,
            'initial_moments':initial_moments,
            't_mat':t_mat,
            'start_time':start_time,
            'end_time':end_time,
            'sim_time':sim_time,
            'extra_mat':extra_mat}
        
    params_with_images=deepcopy(params)
    
    # make these point to the same thing
    params_with_images['saved_input_vectors']=params['saved_input_vectors']
    
    fix_images_directories(params_with_images,parent)
    
    
    if not save_sim_file is None:
        status('Preemtive Save: %s' % save_sim_file,parent)
        zpickle.save(sim,save_sim_file)
    
    
    w=weights[layer]
    m=moments[layer]
    ind_m=individual_moments[layer]
    
    
    t0=time.time()
    last_display_time=t0
    extra_input=[]
    try:
    
        for epoch in range(start_epoch,start_epoch+params['epoch_number']):
            t1=time.time()
            
            extra=train(epoch-start_epoch,params_with_images,
                            w,m,ind_m,extra_input)
        
            if extra:
                extra_mat.append(extra)
                
            
            # copy over mask stuff
            if epoch==start_epoch:
                for i,p in enumerate(params['pattern_input']):
                    params['pattern_input'][i]['mask']=params_with_images['pattern_input'][i]['mask']
    
    
            dt1=time.time()-t1
            dt0=time.time()-t0
            if (time.time()-last_display_time)>params['minimum_print_time']:
                last_display_time=time.time()
                
                frac=(epoch-start_epoch+1.0)/params['epoch_number']
                eta=sec2str(dt0/frac-dt0)
                
                status("%.4f...ETA %s" % (dt1,eta),parent)
            
            sim['moments_mat']=numpy.dstack( (sim['moments_mat'],m) )
            
            test_stimulus_type=params['test_stimulus'][layer]['type']
            
            if test_stimulus_type==1: # test OR single
                
                response_var=test_OR_single(params,weights)
                response_var_list[0]=response_var
                if not response_var:
                    params['test_stimulus'][layer]['type']=0
                else:
                    for r,mat in zip(response_var,response_mat):
                        mat.append(r[0])
    
            t_mat.append(t_mat[-1]+params['iter_per_epoch'])
    
            if params['keep_every_epoch']:
                weights_mat.append(deepcopy(weights))
                individual_moments_mat.append(deepcopy(individual_moments))
               
            if params['display'] and epoch%params['epoch_per_display']==0:
                if parent:
                    parent.Plot(sim)
                else:
                    Plot(sim)
            
            if parent:
                parent.Yield()
                if parent.Stopping():
                    break
                
            if dt0>(60*60*20):   # every 20 minutes
                if not save_sim_file is None:            
                    status('Incremental Save: %s' % (save_sim_file),parent)
                    zpickle.save(sim,save_sim_file)
        
    except KeyboardInterrupt:
        status("Stopping!",parent)
        pass
        
    end_time=time.time()
    sim_time=end_time-start_time
        
    if params['display']:
        if parent:
            parent.Plot(sim)
        else:
            Plot(sim)

    tt=sec2str(time.time()-t0)
    if save_sim_file is None:            
        status('Save: None. Total time %s' % (tt),parent)
    else:
        status('Save: %s. Total time %s' % (save_sim_file,tt),parent)
        zpickle.save(sim,save_sim_file)
       
    return sim 
       
if __name__ == '__main__':

    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-p", "--paramfile",
                      dest="paramfile",
                      help="parameter file to run")
    (options, args) = parser.parse_args()

    run_sim(options.paramfile)
    
