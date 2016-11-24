from __future__ import with_statement

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

def get_version():
    
    d={}
    version_line=''
    with open('version.py') as fid:
        for line in fid:
            if line.startswith('version='):
                version_line=line
    print version_line
    
    exec(version_line,d)
    return d['version']
    

setup(
  name = 'plasticity',
  version=get_version(),
  description="Synaptic Plasticity in Rate-Based Neurons",
  author="Brian Blais",
  ext_modules=[ 
    Extension("train",["./train.pyx"],
    include_dirs = [numpy.get_include()],
    ),
    ],
    
  cmdclass = {'build_ext': build_ext}
)


