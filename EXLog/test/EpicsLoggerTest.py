'''
Created on Dec 11, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger

URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
# URL='crap'
a=EpicsLogger()
a.setName('arman')
a.createOlogClient(name='arman', url=URL, username=USR, password=PSWD)
a.retrieveLogbooks()
print a._existingLogbooks
a.createLogbook(newLogbook='TestLog.2', Owner="Operations")
print a._existingLogbooks
print a.queryLogbookObject(logBook='TestLog')