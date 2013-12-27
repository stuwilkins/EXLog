__author__ = 'arkilic'
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
import unittest
URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')

#URL = "http://localhost:8080/Olog"
#URL2 = "https://localhost:8181/Olog"
logInst = EpicsLogger()
#logInst2 = EpicsLogger()
logInst.createOlogClient('test client', URL, USR, PSWD)
print logInst.retrieveLogbooks()
print logInst.retrieveLogbooks()
# print logInst.find_logEntries(logbook='Operations')
#print logInst.retrieveOlogClient()
# logInst.createLogbook('test logbook', 'tester')
# print logInst.retrieveLogbooks()
# logInst2.createOlogClient('client2',URL2, USR,PSWD)
# logInst2.createLogbook('logbook1','logbook owner')