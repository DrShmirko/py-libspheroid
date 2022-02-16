"""
    Setup file for the libsphrtoids package.
    Copyright Constantine Shmirko (c) 2021
"""
from numpy.distutils.core import Extension

extension = Extension(name='_libspheroid',
                      sources=[ 
                          'spheroid/src/mo_par_DLS.f90',
                          'spheroid/src/DLS_fixget.f90',
                          'spheroid/src/DLS_intrpl.f90',
                          'spheroid/src/DLS_optchr.f90',
                          'spheroid/src/DLS_read_input.f90',
                          'spheroid/src/mo_DLS.f90',
                          'spheroid/src/mo_alloc.f90',
                          'spheroid/src/mo_alloc1.f90',
                          'spheroid/src/mo_intrpl_linear.f90',
                          'spheroid/src/mo_intrpl_spline.f90',
                          'spheroid/src/mo_usea.f90',
                          'spheroid/src/phase_func.f90',
                          'spheroid/src/sizedstr.f90'
                               ],
                      # extra_f90_compile_args=['-fdefault-real-8'],
                      # extra_f77_compile_args=['-fdefault-real-8'],
                      )

if __name__ == "__main__":
    from numpy.distutils.core import setup
    #from setuptools import setup
    setup(name='libspheroids',
          version = '1.0.1',
          author="Constantine Shmirko",
          author_email="kshmirko@gmail.com",
          ext_modules=[extension],
	      #install_requires=['wheel'],
          packages=['libspheroid'],
          package_data={'libspheroid':
              ['KRNLS_arnt_sphrds/*.txt','KRNLS_arnt_sphrs/*.txt']},
          description='',
          long_description=open('README.txt').read()
          )
