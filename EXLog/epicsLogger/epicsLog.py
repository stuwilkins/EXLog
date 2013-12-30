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
#TODO: Keep track of existing property inside a dictionary that as an attribute to class instance. append the newly created entries. this reduces the number of trips to the database
#TODO: Add regular expressions to queries.
#TODO: createLogInstance() must provide an easy way to create logging object for developers
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
        self.__existingTags = list()
        self.__ologEntry = None
        self.__name = None
        self.__pythonLogger = None
        self.__logMode = 'remote'

    def setLogMode(self,mode):
        '''
        Logging is possible both locally(via writing into a log file in a systematic fashion or remote olog server
        Modes: 'local' OR 'remote'
        '''
        if mode == 'local' or mode == 'remote':
            self.__logMode = mode
        else:
            raise ValueError("Invalid log mode")
        
    def retrieveLogMode(self):
        return self.__logMode

    def isOlog(self):
        '''
        Checks whether logging mode is set to remote olog server
        Raises exception if logging mode is set to local. Called in order to assure remote logging inside routines
        '''
        if self.__logMode == 'local':
            raise Exception("Log level is set to local. Set level to server for using Olog functionalities")

    def isLocal(self):
        '''
        Checks whether logging mode is set to local log file.
        Raises exception if logging mode is set to remote. Called in order to assure local logging inside routines
        '''
        if self.__logMode == 'remote':
            raise Exception("Log level is set to server. Set level to local for using local logging functionalities")

    def createLogInstance(self, mode='remote'):
        '''
        createLogInstance() provides a simplified way to create an EpicsLogger instance./
        This routine handles local vs. server logging. Advanced users who would like to/
        customize their applications can still use other EpicsLogger instances in order to create logging instances that satisfy their needs.
        '''
        #check logging mode: try create olog client. check flag returned
        #if local, use createLocalLogger()
        #if local does not work either: finally raise exception
        raise NotImplementedError('Requirements needed for minimum logging given beamline application')
        
    def createPythonLogger(self, name):
        '''
        Creates the local logging instance using native Python Formatter and Handler
        '''
        self.setName(name)
        self.__pythonLogger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/' + str(name) + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.__pythonLogger.addHandler(hdlr)
        self.__pythonLogger.setLevel(logging.INFO)

    def __is_pyLogger(self):
        '''
        Checks whether a native python logger with handler and formatter information has been created
        Return Type: Boolean
        '''
        flag = False
        if self.__pythonLogger is None:
            flag = False
        else:
            flag = True
        return flag

    def createLocalLogger(self, name):
        '''
        This will create a local logging instance where connection to an olog server is not available or preferred.
        '''
        #TODO: create local methods for logging w/o Olog remote server. This must be in a fashion such that this saved
        #information is parsable in the future.
        raise NotImplementedError("Local logging must have similar characteristics with remote olog logging. A set of logbooks, "
                                  "tags, and clients have to be generated.")

    def createOlogClient(self, name, url, username, password):
        '''
        Creates a local logger and Olog client. pythonLogger is a prerequisite for all logging. Once Olog client is \
        successfully created, existing properties, tags, and logbooks are saved locally.
        '''
        self.isOlog()
        self.__is_pyLogger()
        if not self.__is_pyLogger():
            self.createPythonLogger(name)
        try:
            self.__ologClient = OlogClient(url, username, password)
            self.__pythonLogger.info('Olog client created. url:' + str(url) +' user name:' + str(username))
            return 'Olog client created. url:' + str(url) + ' user name:' + str(username)
            self.__composeLogbookList()
            self.__composeTagList()
            self.__composePropList()
        except:
            #TO DO: Once local logger added, prompt user with the choice of local logging once no remote available
            self.__pythonLogger.warning('Unable to create Olog client')
            raise
    
    def is_ologClient(self):
        '''
        Checks whether an OlogClient for EpicsLogger instance is created.
        '''
        self.isOlog()
        if self.retrieveOlogClient() is None:
            raise ValueError("Olog Client not created yet")

    def find(self, **kwds):
        '''
        >>> find(search='*Timing*')
        find logentries with the text Timing in the description

        >>> find(tag='magnets')
        find log entries with the a tag named 'magnets'

        >>> find(logbook='controls')
        find log entries in the logbook named 'controls'

        >>> find(property='context')
        find log entires with property named 'context'

        >>> find(start=str(time.time() - 3600)
        find the log entries made in the last hour
        >>> find(start=123243434, end=123244434)
        find all the log entries made between the epoc times 123243434 and 123244434

        Searching using multiple criteria
        >>> find(logbook='contorls', tag='magnets')
        find all the log entries in logbook 'controls' AND with tag named 'magnets'
        '''
        self.isOlog()
        self.is_ologClient()
        log_entries = self.__ologClient.find(**kwds)
        return log_entries
        pass

    def retrieveOlogClient(self):
        '''
        Returns OlogClient object created. Useful for calling native pyOlog routines
        Usage:
            >>> from pyOlog import Logbook, Attachments
            >>> epicsLoggerInstance = EpicesLogger()
            >>> client = epicsLoggerInstance.retrieveOlogClient()
            >>> sample_logbook = Logbook(name='sample logbook', owner= 'sample owner')
            >>> client.createLogbook(sample_logbook)
        **This is not recommended unless user is has a good understanding of epics logging tools and would like to add/debug pyOlogrs.**
        '''
        self.isOlog()
        return self.__ologClient
                
    def createLogbook(self,newLogbook,Owner):
        '''
        Creates an olog Logbook and adds this logbook name to existing logbook names.
        '''
        self.isOlog()
        self.is_ologClient()
        print self.__existingLogbooks
        if newLogbook in self.__existingLogbooks:
            self.__pythonLogger.info('Olog Logbook ' + str(newLogbook) + ' exists')
            print 'Olog Logbook ' + str(newLogbook) + ' exists'
            self.__ologLogbook = self.__retrieveLogbookObject(name=newLogbook)
        else:
            self.__ologLogbook = Logbook(name = newLogbook, owner = Owner)
            try:
                self.__ologClient.createLogbook(self.__ologLogbook)
                self.__existingLogbooks.append(self.__ologLogbook.getName())
            except:
                self.__pythonLogger.warning('Olog Logbook cannot be created')
                raise
        return None
    
    def retrieveLogbooks(self):
        '''
        Gets and assings "all active logbooks" to self._existingLogbooks
        Returns:  tuple(list of active logbooks)
        '''
        self.isOlog()
        self.is_ologClient()
        logbooks = self.__composeLogbookList()
        return logbooks
    
    def queryLogbook(self,logBook):
        """
        Queries Olog RDB and returns True or False based existince of queried "Logbook Name"
        Returns: Boolean
        """
        self.isOlog()
        self.is_ologClient()
        find_success = False
        log_books = self.retrieveLogbooks()
        if logBook in log_books:
            find_success = True
        else:
            print 'Queried Logbook does not exist'
            raise ValueError('Queried Logbook does not exist')
        return find_success

    def __retrieveLogbookObject(self, name):
        #TODO: Add regular expressions for queries
        '''
        Returns a "Logbook Object" with given "Logbook Name".
        '''
        logbook_objects = self.__ologClient.listLogbooks()
        queried_object = None
        for entry in logbook_objects:
            if name == entry.getName():
                queried_object = entry
                break
        if queried_object is None:
            raise ValueError('Queried LogBook does not exist')
        return queried_object

    def __composeLogbookList(self):
        '''
        Compose a list of Logbook objects on Olog Server.
        '''
        logbookObjects = list()
        logbookNames = list()
        try:
            logbookObjects = self.__ologClient.listLogbooks()
            for entry in logbookObjects:
                logbookNames.append(entry.getName())
        except:
            self.__logLevel = 'local'
            print "Logging Mode:"
            self.__pythonLogger.warning('Olog logbooks cannot be accessed')
            raise
        self.__exlogBookistingLogbooks = logbookNames
        return logbookNames
    
    
    def createTag(self, newTagName, newTagState):
        '''
        Creates an Olog tag.
        '''
        self.isOlog()
        self.is_ologClient()
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
            self.__ologTag = self.__retrieveTagObject(name=newTagName)
        else:
            self.__ologTag = Tag(name = newTagName, state = newTagState)
            try:
                self.__ologClient.createTag(self.__ologTag)
                self.__existingTags.append(self.__ologTag.getName())
            except:
                self.__pythonLogger.warning('Olog Tag can not be created')
                raise
            
    def retrieveTags(self):
            '''
            Returns existing olog tag instances already created
            '''
            self.isOlog()
            self.is_ologClient()
            tags = self.__composeTagList()
            return tags

    def queryTags(self, tag):
        """
        Returns True/False based on existence given "Tag Name"
        """
        self.isOlog()
        self.is_ologClient()
        find_success = False
        tag_list = self.retrieveTags()
        if tag in tag_list:
            find_success = True
        else:
            print 'Queried Tag does not exist'
            raise ValueError('Queried Tag does not exist')
        return find_success
        
    def __retrieveTagObject(self,name):
        tag_objects = self.__ologClient.listTags()
        queried_object = None
        for entry in tag_objects:
            if name == entry.getName():
                queried_object = entry
                break    
        if queried_object is None:
            raise ValueError('Queried LogBook does not exist')
        return queried_object
    
    def __composeTagList(self):
        tag_names = list()
        try:
            tag_objects = self.__ologClient.listTags()
            for entry in tag_objects:
                tag_names.append(entry.getName())
        except:
            raise
        self.__existingTags = tag_names
        return tag_names
    
    
    def verifyPropName(self,name):
        '''
        Returns "None" if user does not want to enter new property name.
        Returns new user defined "property name" if name was in use
        '''
        self.isOlog()
        self.is_ologClient()
        propDict = self.__composePropAttDict()
        if propDict.has_key(name):
            renameResp = raw_input("The name suggested for new Property exists. Rename[y/n]")
            if renameResp == 'y':
                name = raw_input('Prop Name: ')
            else:
                name == None
        return name

    def retrieveExistingPropObjects(self):
        '''
        Returns a list of existing property objects
        '''
        self.isOlog()
        self.is_ologClient()
        self.__existingProperties=self.__ologClient.listProperties()
        return self.__existingProperties

    def __composePropAttDict(self):
        '''
        Returns a dictionary where property names are the "keys" and values are attribute names
        '''
        paDict = dict()
        propObjects = self.retrieveExistingPropObjects()
        for entry in propObjects:
            paDict[entry.getName()] = entry.getAttributeNames()
        return paDict

    def __composePropList(self):
        temp_prop = list()
        try:
            prop_objects = self.__ologClient.listProperties()
            temp_prop = list()
            for entry in prop_objects:
                temp_prop.append(entry.getName())
        except:
            raise

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
        return self.__composePropAttDict()

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