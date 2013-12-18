'''
Created on Dec 11, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
from pyOlog import OlogClient

URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
URL = 'http://webdev.cs.nsls2.local:8080/Olog'


logInstance = EpicsLogger()
logInstance.createOlogClient(name = 'default', url = URL, username = USR, password = PSWD)
# logInstance.createOlogClient(name = 'default2', url = URL, username = USR, password = PSWD)
