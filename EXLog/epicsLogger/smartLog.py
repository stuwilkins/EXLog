"""
Copyright (c) 2014 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.
Created on Jan 13, 2014

@author: Arman Arkilic
"""
from epicsLogger import epicsLog
from EXLog.config.configParser import URL, USR, PSWD, MODE, LOGBOOKS, TAGS, PROPERTIES, OWNER
from epicsLogger.epicsLog import EpicsLogger


def createLogInstance(name):
    logInstance = EpicsLogger()
    logInstance.createPythonLogger(name)
    if MODE == 'local':
        raise NotImplementedError("Local logging w/o remote Olog server will be implemented")
    else:
        logInstance.setLogMode(mode=MODE)
        new_log_mode = logInstance.retrieveLogMode()
        if new_log_mode != 'remote':
            raise ValueError('Invalid Logging Mode[remote/local]')

        logInstance.createOlogClient(name, URL, USR, PSWD)
        print LOGBOOKS
        print TAGS
        print PROPERTIES
        logInstance.createMultipleLogbooks(LOGBOOKS, OWNER)
        logInstance.createMultipleTags(TAGS)

        # logInstance.createProperty(propName=PROPERTIES[0],attributes={'att_name_1':None})
createLogInstance("arman")
