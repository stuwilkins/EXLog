'''
Copyright (c) 2014 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.
Created on Dec 9, 2013
@author: arkilic
'''
from distutils.core import setup
import os
os.environ['EPICS_BASE']='/usr/lib/epics'
os.system('echo $EPICS_BASE')
setup(name='EXLog',
      version='0.1.0',
      description='EPICS eXperimental Logging Library',
      author='Arman Arkilic',
      author_email='arkilic@bnl.gov',
      packages=['EXLog','EXLog.config','EXLog.epicsLogger',
                'EXLog.properties','dummyBroker','EXLog.channelFinder','EXLog.propertyDepot', 'EXLogAPI'])
