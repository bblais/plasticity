#Code from bblais 2014
cdef  rk_state global_state

cpdef  init_by_int(int seed):
    rk_seed(seed, &global_state)

cpdef  init_by_entropy():
    rk_randomseed(&global_state)

cpdef double randu():
    return(rk_double(&global_state))

cpdef double randn():
    return(rk_gauss(&global_state))

cpdef double rande():
    cdef double y
    y=2.0*randu()-1.0
    if y<0.0:
        return log(-y)
    elif y>0.0:
        return -log(y)
    else:
        return 0.0