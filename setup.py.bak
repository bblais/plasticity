# this is from https://github.com/cython/cython/wiki/PackageHierarchy

from __future__ import with_statement

import sys, os, stat, commands
from distutils.core import setup
from Cython.Distutils import build_ext
from distutils.extension import Extension

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except:
    print "You don't seem to have Cython installed. Please get a"
    print "copy from www.cython.org and install it"
    sys.exit(1)

import numpy

def get_version(package):
    
    d={}
    version_line=''
    with open('%s/version.py' % package) as fid:
        for line in fid:
            if line.startswith('version='):
                version_line=line
    print version_line
    exec(version_line,d)
    return d['version']



# scan the  directory for extension files, converting
# them to extension names in dotted notation
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files

def cleanc(dir):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            base,ext=os.path.splitext(path)
            cpath=base+'.c'
            if os.path.isfile(cpath):
                os.remove(cpath)
                print "~~",cpath
        elif os.path.isdir(path):
            cleanc(path)

# generate an Extension object from its dotted name
def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep)+".pyx"
    folder=extName.split(".")[0]
    return Extension(
        extName,
        [extPath,'plasticity/randomkit.c'],
        include_dirs = [numpy.get_include(), ".", "%s/" % folder],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args = ["-O3", "-Wall"],
        extra_link_args = ['-g'],
        )

# get the list of extensions
extNames = scandir("plasticity")
print extNames
cleanc("plasticity")

# and build up the set of Extension objects
print extNames

extensions = [makeExtension(name) for name in extNames]
# finally, we can pass all this to distutils
setup(
  name="plasticity",
  version=get_version('plasticity'),
  description="Synaptic Plasticity in Rate-Based Neurons",
  author="Brian Blais",
  packages=['plasticity',
            'plasticity.dialogs',
            'plasticity.dialogs.waxy'],
  scripts=['plasticity/Plasticity.pyw'],
  
  package_data={'plasticity': ['images/*.*','dialogs/images/*.*',
                                'dialogs/images/learning_rules/*.*','hdf5/*.*']},            
  ext_modules=extensions,
  cmdclass = {'build_ext': build_ext},
)
