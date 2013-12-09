'''
Copyright (c) 2013 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Dec 2, 2013

@author: arkilic
'''
from pyOlog import OlogClient
from pyOlog.OlogDataTypes import Attachment, Logbook, LogEntry, Property, Tag
import logging
from os import path
#TO DO: Keep track of existing property inside a dictionary that as an attribute to class instance. append the newly created entries. this reduces the number of trips to the database

class EpicsLogger():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._ologClient = None
        self._ologLogbook = None
        self._ologTag = None
        self._ologProperty = None
        self._existingProperties = dict()
        self._existingAttributes = dict()
        self._ologEntry = None
        self._name = None
        self._logger = None
    
    def createLocalLogger(self,name):
        self.setName(name)
        self._logger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/' + str(name) + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self._logger.addHandler(hdlr)
        self._logger.setLevel(logging.INFO)

    def getExistingPropObjects(self):
        self._existingProperties=self._ologClient.listProperties()
        return self._existingProperties
            
    def createOlogClient(self, url, username, password):
        self.checkLogger()
        try:
            self._ologClient=OlogClient(url, username, password)
            self._logger.info('Olog client created. url:' + str(url) +' user name:' + str(username))
            print 'Olog client created. url:' + str(url) + ' user name:' + str(username)
        except:
            print 'Could not create client'
            self._logger.warning('Unable to create Olog client')
            raise ValueError('Unable to create Olog Client')

    def getOlogClient(self):
        return self._ologClient

    def createLogbook(self,newLogbook,Owner):
        logbookList = list()
        logbookObjects = list()
        try:
            logbookObjects = self._ologClient.listLogbooks()
        except:
            self._logger.warning('Olog logbooks cannot be accessed')
            raise Exception('Olog logbooks cannot be accessed')
        for entry in logbookObjects:
            logbookList.append(entry.getName())
        if newLogbook in logbookList:
            self._logger.info('Olog Logbook ' + str(newLogbook) + ' exists')
            print 'Olog Logbook ' + str(newLogbook) + ' exists'
        else:
            self._ologLogbook = Logbook(name = newLogbook, owner = Owner)
            try:
                self._ologClient.createLogbook(self._ologLogbook) 
            except:
                self._logger.warning('Olog Logbook cannot be created')
                raise Exception('Olog Logbook cannot be created')
        self._ologLogbook = newLogbook

    def getLogbook(self):
        """
        Returns Olog logbook name as string.
        """
        return self._ologLogbook

    def getLogbookObject(self,logBook):
        """
        Returns Olog Logbook object for a given lobBook name
        """
        queriedLogbook = None
        try:
            logbookList = self._ologClient.listLogbooks()
        except:
            raise Exception("Olog Tags are not accessible. Check your Olog client configuration")
        for entry in logbookList:
            if entry.getName() == logBook:
                queriedLogbook = entry
                break
        if queriedLogbook==None:
            print 'Queried Logbook does not exist'
            raise ValueError('Queried Logbook does not exist')
        return queriedLogbook

    def createTag(self,newTagName,newTagState):
        tagList = list()
        tagObjects = list()
        try:
            tagObjects = self._ologClient.listTags()
        except:
            self._logger.warning('Olog tags cannot be accessed')
            raise Exception('Olog tags cannot be accessed')
        for entry in tagObjects:
            tagList.append(entry.getName())
        if newTagName in tagList:
            self._logger.info('Olog Tag' + str(newTagName) + ' has already been created')
            print 'Olog Tag ' + str(newTagName) + ' has already been created'
        else:
            self._ologTag = Tag(name = newTagName, state = newTagState)
            try:
                self._ologClient.createTag(self._ologTag)
                self._logger.warning('Olog Tag can not be created')
            except:
                raise Exception('Olog Tag can not be created')
        self._ologTag = newTagName

    def getTag(self):
        """
        Returns Olog logbook name as string.
        """
        return self._ologTag

    def getTagObject(self, tag):
        """
        Returns Olog Tag object for a given lobBook name
        """
        queriedTag = None
        try:
            tagList = self._ologClient.listTags()
        except:
            raise Exception("Olog Tags are not accessible!")
        for entry in tagList:
            if entry.getName() == tag:
                queriedTag = entry
                print entry.getName()
                break
        if queriedTag is None:
            raise ValueError('Queried Logbook does not exist')
        return queriedTag

    def verifyPropName(self,name):
        '''
        Returns "None" if user does not want to enter new property name. 
        Returns new user defined "property name" if name was in use
        '''
        propDict = self._composePropAttDict()
        if propDict.has_key(name):
            renameResp = raw_input("The name suggested for new Property exists. Rename[y/n]")
            if renameResp=='y':
                name = raw_input('Prop Name: ')
            else:
                name = None  
        return  name
    
    def _composePropAttDict(self):
        '''
        Returns a dictionary where property names are the "keys" and values are attribute names
        '''
        paDict = dict()
        propObjects = self.getExistingPropObjects()
        for entry in propObjects:
            paDict[entry.getName()] = entry.getAttributeNames()
        return paDict

    def createProperty(self, name, **kwargs):
        '''
        Returns the status of Olog Property creation operation
        Return Type: Boolean
        '''
        createSuccess = False
        property_name = self.verifyPropName(name)
        print property_name
        if property_name is None:
            createSuccess = False
        else:
            prop = Property(name = property_name, attributes = kwargs)
            try:
                self._ologClient.createProperty(prop)
            except:
                raise Exception('Cannot connect to Olog server to create Olog Property')
                self._logger.warning('Cannot connect to Olog server to create Property')
            createSuccess = True
        return createSuccess  
    
    def listProperties(self):
        '''
        Returns a dictionary: {keys=Property Name,values=Attribute Names}
        '''
        return self._composePropAttDict()
     
    def setName(self,name):
        '''
        Sets the name for epicsLogger Instance. In the future this can be changed to iterators.
        '''
        self._name = name

    def getName(self):
        return self._name

    def checkLogger(self):
        if (self._logger == None):
            raise  Exception("Logger has not been created. See createLogger() ")
