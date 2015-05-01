import pylab

def UserPlot(what_is_this,sim):

    ax=pylab.subplot(121)
    ax.hold(False)
    y=sim['weights'][0].ravel()
    pylab.plot(y,'-o')
    pylab.ylabel('weights')
    
    num_moments=sim['moments_mat'].shape[0]
    
    ax=pylab.subplot(122)
    ax.hold(False)
    if num_moments==1:
        pylab.plot(sim['t_mat'],sim['moments_mat'][0,0,:],'-o')
        pylab.ylabel('theta')
    elif num_moments==2:
        pylab.plot(sim['t_mat'],sim['moments_mat'][0,0,:],'b-o')
        ax2=pylab.twinx(ax)
        pylab.plot(sim['t_mat'],sim['moments_mat'][1,0,:],'g-o')
        ax2.yaxis.tick_right()

    else:
        for i in range(num_moments):
            pylab.plot(sim['t_mat'],sim['moments_mat'][i,0,:],'-o')
            ax.hold(True)
    
    

    