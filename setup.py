from setuptools import setup
from setuptools import find_packages
from distutils.core import Extension
from sys import platform as _platform
import sys
import glob
import numpy


DIR = 'pydart2/'

CXX_FLAGS = '-Wall -msse2 -fPIC -std=c++11 -Xlinker -rpath /usr/local/lib '
CXX_FLAGS += '-O3 -DNDEBUG -shared '
CXX_FLAGS += '-g -fno-omit-frame-pointer -fno-inline-functions '
CXX_FLAGS += '-fno-inline-functions-called-once -fno-optimize-sibling-calls '
# CXX_FLAGS += '-DPY_VERSION_HEX=0x03000000'

include_dirs = list()
include_dirs += ['/usr/include']
include_dirs += ['/usr/include/eigen3']

# Fetch python version
python_version = sys.version_info
python_major_version = python_version[0]
python_minor_version = python_version[1]

current_python = "python%d.%d" % (python_major_version, python_minor_version)
print("current_python = %s" % (current_python))
# include_dirs += ['/usr/include/python2.7']
# include_dirs += ['/usr/local/include/python2.7']
include_dirs += ['/usr/include/%s' % current_python]
include_dirs += ['/usr/local/include/%s' % current_python]
include_dirs += ['/usr/include/bullet']
include_dirs += ['/usr/local/include']
include_dirs += ['/usr/local/include/eigen3']
include_dirs += ['/usr/local/include/bullet']
print("numpy.get_include() = %s" % numpy.get_include())
include_dirs += [numpy.get_include()]
# include_dirs += ['/usr/local/lib/%s/dist-packages/numpy/core/include/' %
#                  current_python]
# include_dirs += ['/usr/lib/%s/dist-packages/numpy/core/include/' %
#                  current_python]

libraries = list()
libraries += ['dart', 'dart-gui']
libraries += ['dart-optimizer-ipopt', 'dart-optimizer-nlopt',
              'dart-planning', 'dart-utils', 'dart-utils-urdf']
# libraries += [current_python]
if _platform == "linux" or _platform == "linux2":
    libraries += ['GL', 'glut', 'Xmu', 'Xi']
elif _platform == "darwin":
    libraries += ['GLUT', 'Cocoa', 'OpenGL']
libraries += ['BulletDynamics', 'BulletCollision',
              'LinearMath', 'BulletSoftBody']

swig_opts = ['-c++']
if python_major_version == 3:
    swig_opts.append('-py3')
print("swig_opts: %s" % (str(swig_opts)))

sources = glob.glob(DIR + "/*.cpp")
sources.append(DIR + "pydart2_api.i")
sources = [f for f in sources if "wrap" not in f]  # Safe guard

print("source files:")
for source_file in sources:
    print("    > %s" % source_file)

print("depend files:")
depends = glob.glob(DIR + "/*.h")
depends.append(DIR + "numpy.i")
for depend_file in depends:
    print("    > %s" % depend_file)

MANIFEST_in = "\n".join(["include %s" % f for f in depends])
print("Please check MANIFEST.in is:")
print("============================")
print(MANIFEST_in)
print("============================")

pydart2_api = Extension('_pydart2_api',
                        define_macros=[('MAJOR_VERSION', '1'),
                                       ('MINOR_VERSION', '0')],
                        include_dirs=include_dirs,
                        libraries=libraries,
                        library_dirs=['/usr/local/lib'],
                        extra_compile_args=CXX_FLAGS.split(),
                        swig_opts=swig_opts,
                        sources=sources,
                        depends=depends)

requires = ['numpy', 'PyOpenGL', 'PyOpenGL_accelerate']
if python_major_version == 3:
    requires.append("future")

setup(name='pydart2',
      version='0.5.3',
      description='Python Interface for DART Simulator',
      url='https://github.com/sehoonha/pydart2',
      author='Sehoon Ha',
      author_email='sehoon.ha@gmail.com',
      license='BSD',
      install_requires=requires,
      keywords=['physics', 'robotics', 'simulation'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2 :: Only',
                   'Topic :: Games/Entertainment :: Simulation'],
      packages=find_packages(exclude=['*/pydart2_api.py']),
      ext_modules=[pydart2_api])
