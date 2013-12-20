'''
Created on Dec 11, 2013

@author: arkilic
'''
import unittest
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
from pyOlog import OlogClient,Tag, Property

URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
# URL = 'http://webdev.cs.nsls2.local:8080/Olog'

# 
# a = OlogClient(url=URL, username=USR, password=PSWD)
# prop = Property(name='unit test prop_1', attributes = [])
# a.createProperty(prop)
# tag = Tag(name = 'unit test', state = 'Active')
# # a.createTag(tag)
# print URL
# print USR
# print PSWD
# i = EpicsLogger()
# i.createOlogClient('ar', URL, USR, PSWD)
# # # i.createTag('ar', 'Active')
# # # i.createLogbook(newLogbook = 'Unit test', Owner = 'Unit tester')
# # i.createProperty(name = 'unit test prop')

  
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
        self.logInstance.createOlogClient(name = 'unit tester', url = URL, username = USR, password = PSWD)
        self.logInstance.setLogMode(mode = 'remote')
          
    def testCreateRemoteTag(self):
        try:
            self.logInstance.createTag(newTagName = 'unit test tag' , newTagState = 'Active')
        except:
            raise
      
    def testCreateRemoteLogBook(self):
        pass
      
      
if __name__ == '__main__':
    unittest.main()    
  
# 
# # logInstance = EpicsLogger()
# # logInstance.createOlogClient(name = 'default', url = URL, username = USR, password = PSWD)
# # print logInstance.retrieveLogbooks()
# # # print logInstance.isLocal()
# # print logInstance._composePropAttDict()
# # 
# # 
# # print logInstance.listProperties()
# # print logInstance._retrieveExistingPropObjects()[1]