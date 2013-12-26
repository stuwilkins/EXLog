__author__ = 'arkilic'
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
import unittest
URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')

URL = "http://localhost:8080/Olog"

logInst = EpicsLogger()
logInst.createOlogClient('test client', URL, USR, PSWD)
logInst.retrieveLogbooks()