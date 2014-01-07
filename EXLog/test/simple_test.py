__author__ = 'arkilic'
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
from pyOlog.OlogDataTypes import Property
import unittest
URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
incorrect_url1 = 'http://incorrect_URL'
incorrect_url2 = 'incorrect_URL'
incorrect_usr = 'incorrect tester'
incorrect_pswd = 'None'

logInst = EpicsLogger()
logInst.createOlogClient(name='Unit tester', url=URL, username=USR, password=PSWD)
# a = logInst.retrieveOlogClient().listProperties()
# for entry in a:
#     print entry.getName()
#     print entry.getAttributeValue(entry.getAttributeNames()[0])
# for entry in a:
#     # print entry.getAttributes()
#     print entry.getAttributeValue(entry.getName())
logInst.createProperty('new test', {'arman':None, 'arman.2':None})