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
logInst.createOlogClient(name = 'Unit tester', url=URL, username=incorrect_usr, password=PSWD)

# # print logInst.queryLogbook(logBook='simple_testz')
logInst.createTag(newTagName='Septums')
logInst.createTag(newTagName='test_tag')
# print logInst.retrieveTags()
# print logInst.queryTags(tag='ARMs')
# # print logInst.retrieveLogbooks()
# # print logInst.retrieveLogbooks()
# # print logInst.find_logEntries(logbook='Operations')
# #print logInst.retrieveOlogClient()
# # logInst.createLogbook('test logbook', 'tester')
# # print logInst.retrieveLogbooks()
# # logInst2.createOlogClient('client2',URL2, USR,PSWD)
# # logInst2.createLogbook('logbook1','logbook owner')