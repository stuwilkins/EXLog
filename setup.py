'''
Created on Dec 9, 2013

@author: arkilic
'''
from distutils.core import setup
import os
os.environ['EPICS_BASE']='/usr/lib/epics'
os.system('echo $EPICS_BASE')


setup(name='pyOlog',
      version='0.1.0',
      description='Python Olog Client Lib',
      author='Kunal Shroff',
      author_email='shroffk@bnl.gov',
      packages=['pyOlog']
     )

setup(name='EXLog',
      version='0.1.0',
      description='EPICS eXperimental Logging Library',
      author='Arman Arkilic',
      author_email='arkilic@bnl.gov',
      packages=['epicsLogger']
     )
