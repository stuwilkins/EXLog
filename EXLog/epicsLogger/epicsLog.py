"""
Copyright (c) 2013 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.

Created on Dec 2, 2013

@author: arkilic
"""
import logging
from os import path
import time
import calendar
from EXLog.pyOlog import OlogClient
from EXLog.pyOlog.OlogDataTypes import Attachment, Logbook, LogEntry, Property, Tag
#TODO: Keep track of existing property inside a dictionary that as an attribute to class instance. append the newly created entries. This reduces the number of trips to the database
#TODO: Add regular expressions to queries.
#TODO: Ensure the same attribute is not buffered multiple times before a flush
class EpicsLogger():
    """
    classdocs
    """
    def __init__(self):
        """
        Constructor
        """
        self.__ologClient = None
        self.__ologLogbook = None
        self.__ologTag = None
        self.__ologProperty = None
        self.__existingProperties = dict()
        self.__bufferedProperties = list()
        self.__existingAttributes = dict()
        self.__existingLogbooks = list()
        self.__existingTags = list()
        self.__ologEntry = None
        self.__name = None
        self.__owner = None
        self.__logbookOwner = 'default owner'
        self.__pythonLogger = None
        self.__logMode = 'remote'

    def setLogMode(self, mode):
        """
        Logging is possible both locally(via writing into a log file in a systematic fashion or remote olog server
        Modes: 'local' OR 'remote'
        """
        if mode == 'local' or mode == 'remote':
            self.__logMode = mode
        else:
            raise ValueError("Invalid log mode")
        
    def retrieveLogMode(self):
        return self.__logMode

    def isOlog(self):
        """
        Checks whether logging mode is set to remote olog server
        Raises exception if logging mode is set to local. Called in order to assure remote logging inside routines
        """
        if self.__logMode == 'local':
            raise Exception("Log level is set to local. Set level to server for using Olog functionalities")

    def isLocal(self):
        """
        Checks whether logging mode is set to local log file.
        Raises exception if logging mode is set to remote. Called in order to assure local logging inside routines
        """
        if self.__logMode == 'remote':
            raise Exception("Log level is set to server. Set level to local for using local logging functionalities")

    def createLogInstance(self, mode='remote'):
        """
        createLogInstance() provides a simplified way to create an EpicsLogger instance./
        This routine handles local vs. server logging. Advanced users who would like to/
        customize their applications can still use other EpicsLogger instances in order to create logging instances that\
        satisfy their needs.
        """
        #make sure logbook owner is read from configuration file
        #check logging mode: try create olog client. check flag returned
        #if local, use createLocalLogger()
        #if local does not work either: finally raise exception
        raise NotImplementedError('Requirements needed for minimum logging given beamline application')
        
    def createPythonLogger(self, name):
        """
        Creates the local logging instance using native Python Formatter and Handler
        """
        self.setName(name)
        self.__pythonLogger = logging.getLogger(name)
        hdlr = logging.FileHandler(path.expanduser('~/' + str(name) + '.log'))
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.__pythonLogger.addHandler(hdlr)
        self.__pythonLogger.setLevel(logging.INFO)

    def setOwner(self, owner):
        """
        Sets the owner of the experiment. This is read directly from the configuration file if/
        epicsLogger.smartLog.createLogInstance() is used, However, one can change this on the fly if this changes during/
        the experiement.
        """
        self.__owner = owner

    def retrieveOwner(self):
        """
        Returns experiment owner name
        """
        return self.__owner

    def __is_pyLogger(self):
        """
        Checks whether a native python logger with handler and formatter information has been created
        Return Type: Boolean
        """
        flag = False
        if self.__pythonLogger is None:
            flag = False
        else:
            flag = True
        return flag

    def createLocalLogger(self, name):
        """
        This will create a local logging instance where connection to an olog server is not available or preferred.
        Not yet implemented. This is likely to call an external plugin where user defines their custom logging tools/
        as in pyspec.
        """
        #TODO: create local methods for logging w/o Olog remote server. This must be in a fashion such that this saved
        #information is parsable in the future.
        raise NotImplementedError("Local logging must have similar characteristics with remote olog logging. A set of logbooks, "
                                  "tags, and clients have to be generated.")

    def createOlogClient(self, name, url, username, password):
        """
        Creates a local logger and Olog client. pythonLogger is a prerequisite for all logging. Once Olog client is/
        successfully created, existing properties, tags, and logbooks are saved locally.
        """
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
        """
        Checks whether an OlogClient for EpicsLogger instance is created.
        """
        self.isOlog()
        if self.retrieveOlogClient() is None:
            raise ValueError("Olog Client not created yet")

    def __find(self, **kwds):
        """
        >>> __find(search='*Timing*')
        find logentries with the text Timing in the description

        >>> __find(tag='magnets')
        find log entries with the a tag named 'magnets'

        >>> __find(logbook='controls')
        find log entries in the logbook named 'controls'

        >>> __find(property='context')
        find log entires with property named 'context'

        >>> __find(start=str(time.time() - 3600)
        find the log entries made in the last hour
        >>> __find(start=123243434, end=123244434)
        find all the log entries made between the epoc times 123243434 and 123244434

        Searching using multiple criteria
        >>> __find(logbook='contorls', tag='magnets')
        find all the log entries in logbook 'controls' AND with tag named 'magnets'
        """
        self.isOlog()
        self.is_ologClient()
        log_entries = self.__ologClient.find(**kwds)
        return log_entries

    def delete(self, **kwds):
        #Propmpt user with once deleted can't be created with the same name
        """
        Method to delete a logEntry, logbook, tag
        delete(logEntryId = int)
        >>> delete(logEntryId=1234)

        delete(logbookName = String)
        >>> delete(logbookName = 'logbookName')

        delete(tagName = String)
        >>> delete(tagName = 'myTag')
        # tagName = tag name of the tag to be deleted (it will be removed from all logEntries)

        """
        self.isOlog()
        self.is_ologClient()
        self.__ologClient.delete(**kwds)


    def retrieveOlogClient(self):
        """
        Returns OlogClient object created. Useful for calling native pyOlog routines
        Usage:
            >>> from pyOlog import Logbook, Attachments
            >>> epicsLoggerInstance = EpicesLogger()
            >>> client = epicsLoggerInstance.retrieveOlogClient()
            >>> sample_logbook = Logbook(name='sample logbook', owner= 'sample owner')
            >>> client.createLogbook(sample_logbook)
        **This is not recommended unless user is has a good understanding of epics logging tools and would like to add/debug pyOlogrs.**
        """
        self.isOlog()
        return self.__ologClient

    def createLogbook(self,newLogbook,**kwargs):
        """
        Creates an olog Logbook and adds this logbook name to existing logbook names. createLogbook() appends names of /
        already existing logbooks into self.__existingLogbooks attribute and this way keeps a local copy minimizing number/
        of trips to the database.
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        used_logbook = None
        if kwargs.has_key('owner'):
            self.__logbookOwner = kwargs['owner']
        self.__existingLogbooks = self.retrieveLogbooks()
        if newLogbook in self.__existingLogbooks:
            self.__pythonLogger.info('Olog Logbook ' + str(newLogbook) + ' exists')
            self.__ologLogbook = self.__retrieveLogbookObject(name=newLogbook)
            return 'Olog Logbook ' + str(newLogbook) + ' exists'
        else:
            self.__ologLogbook = Logbook(name=newLogbook, owner=self.__logbookOwner)
            try:
                self.__ologClient.createLogbook(self.__ologLogbook)
                self.__existingLogbooks.append(self.__ologLogbook.getName())
            except:
                self.__pythonLogger.warning('Olog Logbook cannot be created')
                raise

    def createMultipleLogbooks(self, logbookList, owner):
        """
        Allows user to create multiple logbooks. The owner of multiple logbooks must be the same.
        """
        #TODO: Make it possible to create multiple logbooks with different owners
        for entry in logbookList:
            self.createLogbook(newLogbook=entry, owner=owner)

    def retrieveLogbooks(self):
        """
        Gets and assings "all active logbooks" to self._existingLogbooks
        Returns:  tuple(list of active logbooks)
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        logbooks = self.__composeLogbookList()
        return logbooks
    
    def queryLogbook(self,logBook):
        """
        Queries Olog RDB and returns True or False based existence of queried "Logbook Name"
        Returns: Boolean
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        find_success = False
        log_books = self.retrieveLogbooks()
        if logBook in log_books:
            find_success = True
        else:
            raise ValueError('Queried Logbook does not exist')
        return find_success

    def __retrieveLogbookObject(self, name):
        #TODO: Add regular expressions for queries
        """
        Returns a "Logbook Object" with given "Logbook Name". This is useful in order to work on the actual Olog Data Type/
        that provides deeper access to the api under EXLog.
        """
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
        """
        Compose a list of Logbook objects on Olog Server.
        """
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
        self.__existingLogbooks = logbookNames
        return logbookNames

    def createTag(self, newTagName):
        """
        Creates an Olog tag.
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        tag_list = list()
        try:
            tagObjects = self.__ologClient.listTags()
        except:
            self.__pythonLogger.warning('Olog tags cannot be accessed')
            raise Exception('Olog tags cannot be accessed')
        for entry in tagObjects:
            tag_list.append(entry.getName())
        if newTagName in tag_list:
            self.__pythonLogger.info('Olog Tag' + str(newTagName) + ' has already been created')
            self.__ologTag = self.__retrieveTagObject(name=newTagName)
            return 'Olog Tag ' + str(newTagName) + ' has already been created'
        else:
            self.__ologTag = Tag(name=newTagName, state='Active')
            try:
                self.__ologClient.createTag(self.__ologTag)
                # self.__existingTags.append(self.__ologTag.getName())
            except:
                self.__pythonLogger.warning('Olog Tag can not be created')
                raise

    def createMultipleTags(self, tagList):
        for entry in tagList:
            self.createTag(newTagName=entry)

    def retrieveTags(self):
            '''
            Returns existing olog tag instances already created
            '''
            self.isOlog()
            self.is_ologClient()
            self.__is_pyLogger()
            tags = self.__composeTagList()
            return tags

    def queryTags(self, tag):
        """
        Returns True/False based on existence given "Tag Name"
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
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
    
    def createProperty(self, propName, attributes):
        """
        Creates a remote Olog property
        """
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        property_names = self.retrievePropertyNames()
        if propName in property_names:
            #Need to verify an attribute. Compose attribute dictionary. update values if they exist
            new_attributes = self.__composeAttributeDict(propName, attributes)
            self.__add2ExistingProperty(propName, new_attributes)
        else:
            prop = Property(name=propName,attributes=attributes)
            try:
                self.__ologClient.createProperty(prop)
                self.__ologProperty = prop
            except:
                self.__pythonLogger.info('Remote Property can not be created')
                raise

    def createMultipleProperties(self, properties, prop_att_dict):
        prop_names = properties
        attribute_dict = dict()
        for entry in prop_names:
            att_list = prop_att_dict[entry]
            for item in att_list:
                attribute_dict[item] = None
            try:
                self.createProperty(entry, attribute_dict)
            except:
                self.__pythonLogger.warning('Property cannot be created')
                raise

    def __add2ExistingProperty(self, prop_name, attribute_dict):
        """
        Adds non-existing attributes to a property
        """
        prop = Property(name=prop_name, attributes=attribute_dict)
        try:
            self.__ologClient.createProperty(prop)
            self.__pythonLogger.info('Property ' + str(prop_name) + ' updated')
        except:
            self.__pythonLogger.warning('Property cannot be created')
            raise

    def __composeAttributeDict(self, prop_name, attributes):
        """
        Checks whether an attribute exists for given property. Returns a dictionary of non-existing attributes
        """
        property_object = self.__retrievePropertyObject(name=prop_name)
        existing_attributes = property_object.getAttributeNames()
        new_attribute_dict = dict()
        for entry in attributes:
            if entry in existing_attributes:
                self.__pythonLogger.info('Attribute ' + str(entry) + ' exists')
            else:
                new_attribute_dict[entry] = None
        return new_attribute_dict

    def retrievePropertyNames(self):
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        self.__existingProperties = self.__composePropertyDict()
        return self.__existingProperties.keys()

    def retrievePropertyWithAttributes(self):
        self.is_ologClient()
        self.is_ologClient()
        self.__is_pyLogger()
        return self.__composePropertyDict()

    def queryProperties(self,property):
        self.isOlog()
        self.is_ologClient()
        self.__is_pyLogger()
        find_success = False
        properties = self.retrievePropertyNames()
        if property in properties:
            find_success = True
        else:
            raise ValueError('Queried Property does not exist')
        return find_success

    def retrieveAttributeValues(self, property_object, attName):
        """
        Given a Property object and attribute name, this routine returns the associated attribute value./
        Useful for consuming log entries found as a result of queries
        """
        attribute_names = property_object.getAttributeNames()
        value = None
        for entry in attribute_names:
            temp = str(entry)
            if temp == attName:
                try:
                    value = property_object.getAttributeValue(attName)
                except:
                    raise
                break
            else:
                value = 'N/A'
        if value == 'N/A':
            raise ValueError('Attribute for given property does not exist.')
        return value

    def retrieveMultipleAttributeValues(self, property_object, attList):
        """
        Given a Property object and a list of attribute names of this property, this routine provides attribute values
        """
        value_dict = dict()
        for entry in attList:
            val = self.retrieveAttributeValues(property_object=property_object, attName=entry)
            value_dict[entry] = val
        return value_dict

    def __retrievePropertyObject(self, name):
        queried_prop = None
        property_objects = self.__ologClient.listProperties()
        for entry in property_objects:
            if entry.getName() == name:
                queried_prop = entry
                break
        if queried_prop is None:
            raise ValueError('Queried property does not exist')
        return queried_prop

    def __composePropertyDict(self):
        property_dict = dict()
        property_objects = self.__ologClient.listProperties()
        for entry in property_objects:
            property_dict[entry.getName()] = entry.getAttributeNames()
        return property_dict

    def capture(self, propname, **kwds):
        attributeDict = kwds
        tba_att = dict()
        existing_prop_att = self.retrievePropertyWithAttributes()
        new_att_names = attributeDict.keys()
        existing_prop_names = existing_prop_att.keys()
        if propname in existing_prop_names:
            existing_atts = existing_prop_att[propname]
            for entry in new_att_names:
                if entry in existing_atts:
                    tba_att[entry] = attributeDict[entry]
                else:
                    raise ValueError('Attribute field for given property does not exist.Add attribute to property')
        else:
            raise ValueError('Property does not exist. Please create a property before capture()')
        prop = Property(propname, tba_att)
        self.__bufferedProperties.append(prop)

    def get_buffered_properties(self):
        return self.__bufferedProperties

    def flush(self):
        self.__bufferedProperties == list()

    def log(self, description, owner=None, logbooks=[], tags=[], attachments=[], id=None):
        """
        Provides user a way to create a log entry using the configuration parameters
        """
        owner = self.retrieveOwner()
        if owner is None:
            raise ValueError('Please specify an owner for this log entry')
        else:
            composed_log_entry = self.__composeLogEntry(description, owner, logbooks, tags, attachments, id)
            try:
                self.__ologClient.log(composed_log_entry)
                self.__bufferedProperties = list()
            except:
                raise

    def __composeLogEntry(self, text, owner, logbooks, tags=[], attachments=[], id=None):
        """
        Prepares log entry. Simplifies logging for users
        """
        #TODO: Use URI explorer to determine whether attachments exist or not
        logbookList = list()
        tagList = list()
        attachmentList = list()
        self.__verifyLogId(id)
        for entry in logbooks:
            if self.queryLogbook(logBook=entry):
                logbookList.append(self.__retrieveLogbookObject(name=entry))
        for entry in tags:
            if self.queryTags(tag=entry):
                tagList.append(self.__retrieveTagObject(name=entry))
        for entry in attachments:
            attachmentList.append(Attachment(file=entry))
        logEntry = LogEntry(text=text, owner=owner, logbooks=logbookList, tags=tagList,
                            properties=self.__bufferedProperties, attachments=attachmentList, id=id)
        return logEntry

    def __verifyLogId(self, id):
        if id is None:
            pass
        else:
            log_entry = self.find(id=id)
            if log_entry==[]:
                raise ValueError('A log entry with specified ID does not exist')

    def __loggingTime(self, id, createTime, modifyTime):
        """
        Obsolete for now.
        This routine is implemented with logging time for local logging only.\
        Remote Olog logging uses json time stamping methods passed from MySQL db
        """
        result = dict()
        if id is None:
            if createTime is None:
                createTime = calendar.timegm(time.gmtime())
            result['createTime'] = createTime
            result['modifyTime'] = None
        else:
            existing_log = self.find(id=id)
            result['createTime'] = int((existing_log[0].getCreateTime())/1000)
            if modifyTime is None:
                modifyTime = int(calendar.timegm(time.gmtime()))
            result['modifyTime'] = modifyTime
        return result

    def findLog(self, **kwds):
        """
        Allows user to find a log entry
        """
        #TODO: Add attachment log search. use value = ... case as in attribute values
        search_params = kwds.keys()
        if len(search_params) == 1 and 'tag' in search_params:
            result = self.__find(tag=kwds['tag'])
        elif len(search_params) == 1 and 'property' in search_params:
            result = self.__find(property=kwds['property'])
        elif len(search_params) == 1 and 'attribute' in search_params:
            result = self.__find(attribute=kwds['attribute'])
        elif len(search_params) == 1 and 'attachment' in search_params:
            result = self.__find(attachment=kwds['attachment'])
        elif len(search_params) == 1 and 'description' in search_params:
            result = self.__find(text=kwds['description'])
        elif len(search_params) == 2 and 'property' in search_params and 'tag' in search_params:
            result = self.__find(property=kwds['property'],
                               tag=kwds['tag'])
        elif len(search_params) == 2 and 'property' in search_params and 'attribute' in search_params:
            result = self.__find(property=kwds['property'],
                               attribute=kwds['attribute'])
        elif len(search_params) == 2 and 'logbook' in search_params and 'tag' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               tag=kwds['tag'])
        elif len(search_params) == 2 and 'logbook' in search_params and 'property' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               property=kwds['property'])
        elif len(search_params) == 2 and 'logbook' in search_params and 'attachment' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               attachment=kwds['attachment'])
        elif len(search_params) == 2 and 'logbook' in search_params and 'attribute' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               attribute=kwds['attribute'])
        elif len(search_params) == 3 and 'logbook' in search_params and 'property' in search_params and 'attribute' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               property=kwds['property'],
                               attribute=kwds['attribute'])
        elif len(search_params) == 3 and 'property' in search_params and 'attribute' in search_params and 'value' in search_params:
            result = self.__find(**{str(kwds['property']) + '.'+str(kwds['attribute']): str(kwds['value'])})
        elif len(search_params) == 3 and 'logbook' in search_params and 'property' in search_params and 'tag' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               property=kwds['property'],
                               tag=kwds['tag'])
        elif len(search_params) == 3 and 'logbook' in search_params and 'description' in search_params and 'tag' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               text=kwds['description'],
                               tag=kwds['tag'])
        elif len(search_params) == 3 and 'logbook' in search_params and 'description' in search_params and 'property' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               text=kwds['description'],
                               property=kwds['property'])
        elif len(search_params) == 4 and 'logbook' in search_params and 'description' in search_params and 'property' in search_params and 'tag' in search_params:
            result = self.__find(logbook=kwds['logbook'],
                               text=kwds['description'],
                               property=kwds['property'],
                               tag=kwds['tag'])
        elif len(search_params) == 4 and 'logbook' in search_params and 'property' in search_params and 'attribute' in search_params and 'value' in search_params:
            result = self.__find(**{kwds['property'] + '.'+kwds['attribute']: str(kwds['value']), 'logbook': kwds['logbook']})
        elif len(search_params) == 4 and 'tag' in search_params and 'property' in search_params and 'attribute' in search_params and 'value' in search_params:
            result = self.__find(**{kwds['property'] + '.'+kwds['attribute']: str(kwds['value']), 'tag': kwds['tag']})
        elif len(search_params) == 4 and 'description' in search_params and 'pro perty' in search_params and 'attribute' in search_params and 'value' in search_params:
            result = self.__find(**{kwds['property'] + '.'+kwds['attribute']: str(kwds['value']), 'text': kwds['description']})
        elif len(search_params) == 4 and 'attachment' in search_params and 'property' in search_params and 'attribute' in search_params and 'value' in search_params:
            result = self.__find(**{str(kwds['property']) + '.'+str(kwds['attribute']): str(kwds['value']), 'attachment': kwds['attachment']})
        else:
            raise NotImplementedError('Log entry search for this case is not yet implemented')
        if result == []:
            raise ValueError('No logs with given parameters found')
        return result

    def setName(self,name):
        """
        Sets the name for epicsLogger Instance. In the future this can be changed to iterators.
        """
        self.__name = name

    def getName(self):
        return self.__name

    def checkLogger(self):
        if (self.__pythonLogger == None):
            raise  Exception("Logger has not been created. See createLogger() ")