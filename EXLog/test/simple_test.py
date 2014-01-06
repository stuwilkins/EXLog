__author__ = 'arkilic'
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
import unittest
URL=_conf.get('user_config','url')
USR=_conf.get('user_config','user')
PSWD=_conf.get('user_config','password')
incorrect_url1 = 'http://incorrect_URL'
incorrect_url2 = 'incorrect_URL'
incorrect_usr = 'incorrect tester'
incorrect_pswd = 'None'
print URL
#URL = "http://localhost:8080/Olog"
# URL2 = "https://localhoest:8181/Olog"
logInst = EpicsLogger()

#logInst2 = EpicsLogger()
# logInst.createOlogClient('test client', URL, USR, PSWD)
# logInst.createOlogClient('unit tester', URL,incorrect_usr,incorrect_pswd)
# 
# # logInst.setLogMode(mode='remote')
# # print logInst.retrieveLogMode()
# # logInst.createLocalLogger(name='default')
# # print logInst.retrieveOlogClient()
# print logInst.retrieveLogbooks()
# logInst.createLogbook(newLogbook='simple_test', Owner='tester')
# print logInst.retrieveLogbooks()

# logInst.createOlogClient('unit tester', incorrect_url1,incorrect_usr,incorrect_pswd)
logInst.createOlogClient(name = 'Unit tester', url=URL, username=USR, password=PSWD)

# # print logInst.queryLogbook(logBook='simple_testz')
logInst.createTag(newTagName='Septums')
logInst.createTag(newTagName='test_tag')
# print logInst.retrieveTags()
# print logInst.queryTags(tag='ARMs')
# # print logInst.retrieveLogbooks()
# # print logInst.retrieveLogbooks()
# # print logInst.find_logEntries(logbook='Operations')
# #print logInst.retrieveOlogClient()
# print logInst.createLogbook('test logbook', 'tester')
# print logInst.delete(logbookName='test logbook')
# logInst.retrievePropertyNames()
# logInst.createProperty(propName='unit test', attributes={'Attribute_1':1,'arnab':1})
# logInst.createProperty(propName=' test', attributes={'Attribute_3':1,'armans':1})
# print logInst.queryProperties(property='test')
# logInst.modifyProperty('test_',{'Attribute #1':None, 'Attribute 2':None})
# logInst.modifyProperty('arman',{'Attribute_1':None,'arnab':1})
# a = ['arnab', 'Attribute_1']
# b = {'Attribute_1','arnab'}
# print set(a)
# print set(b)
logInst.retrieveAttributeValues('new test2')
# print set(a)&set(b)
# # print logInst.retrieveLogbooks()
# # logInst2.createOlogClient('client2',URL2, USR,PSWD)
# # logInst2.createLogbook('logbook1','logbook owner')