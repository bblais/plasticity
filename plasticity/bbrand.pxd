cdef extern from "math.h":
    double log(double)

cdef extern from "randomkit.h":
    ctypedef struct rk_state: 
        pass
    ctypedef struct rk_error: 
        pass
    
    void rk_seed(unsigned long seed, rk_state *state)
    rk_error rk_randomseed(rk_state *state)
    double rk_double(rk_state *state)
    double rk_gauss(rk_state *state)


cpdef  init_by_int(int seed)
cpdef  init_by_entropy()
cpdef double randu()
cpdef double randn()
cpdef double rande()
