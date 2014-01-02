'''
Created on Dec 11, 2013

@author: arkilic
'''
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
import unittest
import requests

URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')

# URL = "http://localhost:8080/Olog
print URL
class TestSetLogEnvironment(unittest.TestCase):

    def setUp(self):
        self.logInstance = EpicsLogger()

    def testSetLogMode(self):
        """
        Logging mode test:
        Default mode must be remote
        Switching between local and remote logging is possible
        No other modes allowed except "remote" and "local"
        Smart createLogInstance NotImplementedError
        """
        invalid_logMode = 'invalid_mode'
        self.assertEqual(self.logInstance.retrieveLogMode(),'remote','Default logging mode must be remote')
        self.logInstance.setLogMode(mode='local')
        self.assertRaises(Exception,self.logInstance.isOlog,'Once log mode is set to local, remote operations are not allowed')
        self.assertEqual(self.logInstance.retrieveLogMode(), 'local', 'Logging mode can not be set')
        self.logInstance.setLogMode(mode='remote')
        self.assertRaises(Exception,self.logInstance.isLocal)
        self.assertEqual(self.logInstance.retrieveLogMode(), 'remote', 'Logging mode can not be set')
        self.assertRaises(ValueError, self.logInstance.setLogMode, invalid_logMode)
        self.assertRaises(NotImplementedError, self.logInstance.createLogInstance, 'local')

    def testCreateRemoteClient(self):
        """
        Simple test to create a ologClient:
            Create client with incorrect URL (denoting http), Username, and Password
            Create client with incorrect URL (no protocol denoted), Username and Password
            Create client with correct URL, incorrect Username, and Password and create a Logbook
        """
        incorrect_url1 = 'http://incorrect_URL'
        incorrect_url2 = 'incorrect_URL'
        incorrect_usr = 'incorrect tester'
        incorrect_pswd = 'None'
        sample_logbookName = 'test logbook'
        sample_logbookOwner = 'test owner'
        self.assertRaises(requests.exceptions.ConnectionError, self.logInstance.createOlogClient, 'unit tester', incorrect_url1, incorrect_usr, incorrect_pswd)
        self.assertRaises(requests.exceptions.MissingSchema, self.logInstance.createOlogClient, 'unit tester', incorrect_url2, incorrect_usr, incorrect_pswd)
        self.logInstance.createOlogClient(name='Unit tester', url = URL, username = incorrect_usr, password = PSWD)
        self.assertRaises(requests.exceptions.SSLError, self.logInstance.createLogbook, sample_logbookName, sample_logbookOwner)

    def testCreateLocalClient(self):
        """
        Test to create a local logging client:
            Not yet implemented
        """
        self.assertRaises(NotImplementedError, self.logInstance.createLocalLogger,'unit test')

class TestCreateRemoteOlogData(unittest.TestCase):

    def setUp(self):
        """
        Create an EpicsLogger instance, set log mode to remote and create an Olog client to carry on logging tasks
        """
        self.logInstance = EpicsLogger()
        self.logInstance.setLogMode(mode='remote')
        self.logInstance.createOlogClient(name='unit tester', url=URL, username=USR, password=PSWD)

    def testCreateRemoteTag(self):
        """
        Test creating a tag. The tag name is randomly generated to avoid unnecessary entries.
        """
        try:
            self.logInstance.createTag(newTagName='unit test tag')
        except:
            raise
        self.logInstance.delete(tagName='unit test tag')
        #clean the tag once done : set state to inactive

    def testCreateRemoteLogBook(self):
        """
        Test to create Olog Logbook:
            Try creating a logbook with a random unique name
            Try creating an existing logbook
        """
        pass

    def testCreateRemoteProperty(self):
        pass

    def testCreateRemoteLogEntry(self):
        pass

class TestQueryRemoteOlogData(unittest.TestCase):

    def setUp(self):
        self.logInstance = EpicsLogger()
        self.logInstance.setLogMode(mode='remote')
        self.logInstance.createOlogClient(name='unit tester', url=URL, username=USR, password=PSWD)


    def testQueryOlogClient(self):
        pass

    def testQueryLogbook(self):
        pass

    def testQueryTag(self):
        pass

    def testQueryPropery(self):
        pass

    def testQueryLogEntry(self):
        pass

class TestQueryRemoteLogEntries(unittest.TestCase):

    def setUp(self):
        pass

    def testCreateLogWithAttachments(self):
        pass




if __name__ == '__main__':
    unittest.main()