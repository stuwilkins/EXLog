__author__ = 'arkilic'
from pyOlog._conf import _conf
from epicsLogger.epicsLog import EpicsLogger
from pyOlog.OlogDataTypes import LogEntry, Logbook, Tag
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
client = logInst.retrieveOlogClient()

# logInst.createProperty('new test', {'arman':None, 'arman.2':None})
# lbook = Logbook(name='Simple Test', owner='arkilic')
# tag = Tag(name='simple test tag',state='Active')
# client.createTag(tag)
# client.createLogbook(lbook)
logInst.log(description='New_7.4.1 API log attempt',owner='arkilic',
            logbooks=['Operations'],tags=['Bumps'],properties=['new test'],id=101)
print logInst.find(text="New_7.4 API log attempt")[0].getId()

# print logInst.find(id=)[0].getCreateTime()
# print logInst.find(id=99)[0].getModifyTime()
# print logInst.find(id=100)[0].getCreateTime()
# print logInst.find(id=100)[0].getModifyTime()
# logInst.verifyLogId(100)