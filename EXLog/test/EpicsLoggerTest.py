'''
Created on Dec 11, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
import unittest
URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')

URL = "http://localhost:8080/Olog"

class TestCreateClient(unittest.TestCase):

    def testCreateRemoteClient(self):
        '''
        Simple test to create a ologClient
        '''
        logInstance = EpicsLogger()
        logInstance.createOlogClient(name = 'Unit tester', url = URL, username = USR, password = PSWD)

    def testCreateLocalClient(self):
        pass

class TestCreateRemoteOlogData(unittest.TestCase):

    def setUp(self):
        self.logInstance = EpicsLogger()
        self.logInstance.setLogMode(mode = 'server')
        self.logInstance.createOlogClient(name = 'unit tester', url = URL, username = USR, password = PSWD)

    def testCreateRemoteTag(self):
        try:
            self.logInstance.createTag(newTagName = 'unit test tag' , newTagState = 'Active')
        except:
            raise

    def testCreateRemoteLogBook(self):
        pass


if __name__ == '__main__':
    unittest.main()
























# a = OlogClient(URL, USR, PSWD)
# tag = Tag(name='1st', state="Active")
# a.createTag(tag)
# log = Logbook(name='Trial', owner='unittest')
# a.createLogbook(log)
# a=EpicsLogger()
# a.setName('arman')
# a.createOlogClient(name='arman', url=URL, username=USR, password=PSWD)
# a.retrieveLogbooks()
# print a._existingLogbooks
# a.createLogbook(newLogbook='TestLog.2', Owner="Operations")
# print a._existingLogbooks
# print a.queryLogbookObject(logBook='TestLog')