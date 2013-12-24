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
#TO DO: Add regular expressions to queries.
class EpicsLogger():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.__ologClient = None
        self.__ologLogbook = None
        self.__ologTag = None
        self.__ologProperty = None
        self.__existingProperties = dict()
        self.__existingAttributes = dict()
        self.__existingLogbooks = list()
        self.__ologEntry = None
        self.__name = None
        self.__pythonLogger = None
        self.__logMode = 'server'

    def setLogMode(self,mode):
        if mode == 'local' or mode == 'server':
            self.__logMode = mode
        else:
            raise ValueError("Invalid log mode")

    def isOlog(self):
        if self.__logMode == 'local':
            raise Exception("Log level is set to local. Set level to server for using Olog functionalities")

    def isLocal(self):
        if self.__logMode == 'server':
            raise Exception("Log level is set to server. Set level to local for using local logging functionalities")

    def createLogInstance(self):
        '''
        createLogInstance() provides a simplified way to create an EpicsLogger instance./
        This routine handles local vs. server logging. Advanced users who would like to/
        customize their applications can still use other EpicsLogger instances in order to create logging instances that satisfy their needs.
        '''
        #check logging mode: try create olog client. check flag returned
        #if local, use createLocalLogger()
        #if local does not work either: finally raise exception
        pass

    def createPythonLogger(self,name):
        '''
        Creates the local logging instance using native python formatter and handler
        '''
        self.setName(name)
        self.__pythonLogger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/' + str(name) + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.__pythonLogger.addHandler(hdlr)
        self.__pythonLogger.setLevel(logging.INFO)
    
    def createLocalLogger(self,name): 
        #TODO: create a default user for machine based logging into a local file. Later this file needs to be parsable
        raise NotImplementedError("This has similar attributes to olog client a set of logbooks, "
                                  "tags and clients have to be generated.")

    def retrieveExistingPropObjects(self):
        '''
        Returns a list of existing property objects
        '''
        self.__existingProperties=self.__ologClient.listProperties()
        return self.__existingProperties

    def createOlogClient(self, name, url, username, password):
        '''
        Creates a local logger and Olog client. pythonLogger is a prerequisite for all logging. Once Olog client is successfully created, existing properties, tags, and logbooks are saved locally.
        '''
        self.isOlog()
        self.createPythonLogger(name)
        try:
            self.__ologClient = OlogClient(url, username, password)
            print self.__ologClient
            self.__pythonLogger.info('Olog client created. url:' + str(url) +' user name:' + str(username))
            print 'Olog client created. url:' + str(url) + ' user name:' + str(username)
            self.__existingLogbooks = self. __composeLogbookList()
        except:
            print 'Client could not be created'
            logModeResp = raw_input('Connection to Olog Server is not successful. Logging Mode Local?[y/n]')
            if logModeResp == 'y':
                self.setLogMode('local')
            else:
                self.__pythonLogger.warning('Unable to create Olog client')
            raise
                
    def retrieveLogbooks(self):
        '''
        Assigns active logbooks to self._existingLogbooks.
        '''
        self.isOlog()
        logbookObjects = list()
        self.__existingLogbooks = list()
        try:
            logbookObjects = self.__ologClient.listLogbooks()
            for entry in logbookObjects:
                self.__existingLogbooks.append(entry.getName())
            return self.__existingLogbooks
        except:
            self.__pythonLogger.warning('Olog logbooks cannot be accessed')
            raise Exception('Olog logbooks cannot be accessed')
        
    def createLogbook(self,newLogbook,Owner):
        '''
        Creates an olog Logbook
        '''
        self.isOlog()
        self.retrieveLogbooks()
        print self.__existingLogbooks
        if newLogbook in self.__existingLogbooks:
            self.__pythonLogger.info('Olog Logbook ' + str(newLogbook) + ' exists')
            print 'Olog Logbook ' + str(newLogbook) + ' exists'
        else:
            self.__ologLogbook = Logbook(name = newLogbook, owner = Owner)
            try:
                self.__ologClient.createLogbook(self.__ologLogbook)
                self.__existingLogbooks.append(self.__ologLogbook.getName())
            except:
                self.__pythonLogger.warning('Olog Logbook cannot be created')
                raise
        self.__ologLogbook = newLogbook

    def retrieveLogbookObject(self,name):
        logbook_objects = self.__ologClient.listLogbooks()
        queried_object = None
        for entry in logbook_objects:
            try:
                if name == entry.getName():
                    queried_object = entry
                    break
            except:
                raise
        if queried_object is None:
            raise ValueError('Queried LogBook does not exist')
        return queried_object

    def queryLogbookObject(self,logBook):
        """
        Returns Olog Logbook object for a given "LogBook Name"
        """
        find_success = False
        queriedLogbook = None
        self.retrieveLogbooks()
        for entry in self.__existingLogbooks:
            if entry.getName() == logBook:
                queriedLogbook = entry
                find_success = True
                break
        if queriedLogbook is None:
            print 'Queried Logbook does not exist'
            raise ValueError('Queried Logbook does not exist')
        return find_success

    def __composeLogbookList(self):
        '''
        Compose a list of Logbook objects on Olog Server.
        '''
        logbookObjects = list()
        try:
            logbookObjects = self.__ologClient.listLogbooks()
        except:
            self.__logLevel = 'local'
            print "Logging Mode:"
            self.__pythonLogger.warning('Olog logbooks cannot be accessed')
        return logbookObjects

    def createTag(self,newTagName,newTagState):
        '''
        Creates an Olog tag.
        '''
        self.isOlog()
        tagList = list()
        tagObjects = list()
        try:
            tagObjects = self.__ologClient.listTags()
        except:
            self.__pythonLogger.warning('Olog tags cannot be accessed')
            raise Exception('Olog tags cannot be accessed')
        for entry in tagObjects:
            tagList.append(entry.getName())
        if newTagName in tagList:
            self.__pythonLogger.info('Olog Tag' + str(newTagName) + ' has already been created')
            print 'Olog Tag ' + str(newTagName) + ' has already been created'
        else:
            self.__ologTag = Tag(name = newTagName, state = newTagState)
            try:
                self.__ologClient.createTag(self.__ologTag)
                self.__pythonLogger.warning('Olog Tag can not be created')
            except:
                raise Exception('Olog Tag can not be created')
        self.__ologTag = newTagName

    def queryTagObject(self, tag):
        """
        Returns Olog Tag object for a given tag name
        """
        queriedTag = None
        try:
            tagList = self.__ologClient.listTags()
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
        propDict = self.__composePropAttDict()
        if propDict.has_key(name):
            renameResp = raw_input("The name suggested for new Property exists. Rename[y/n]")
            if renameResp=='y':
                name = raw_input('Prop Name: ')
            else:
                name == None
        return name

    def __composePropAttDict(self):
        '''
        Returns a dictionary where property names are the "keys" and values are attribute names
        '''
        paDict = dict()
        propObjects = self.retrieveExistingPropObjects()
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
                self.__ologClient.createProperty(prop)
            except:
                raise Exception('Cannot connect to Olog server to create Olog Property')
                self.__pythonLogger.warning('Cannot connect to Olog server to create Property')
            createSuccess = True
        return createSuccess

    def listProperties(self):
        '''
        Returns a dictionary of properties and their attributes: {keys=Property Name,values=Attribute Names}
        '''
        return self._composePropAttDict()

    def setName(self,name):
        '''
        Sets the name for epicsLogger Instance. In the future this can be changed to iterators.
        '''
        self.__name = name

    def getName(self):
        return self.__name

    def checkLogger(self):
        if (self.__pythonLogger == None):
            raise  Exception("Logger has not been created. See createLogger() ")