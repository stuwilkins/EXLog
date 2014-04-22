"""
Copyright (c) 2014 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.
Created on Jan 13, 2014

@author: Arman Arkilic
"""
from EXLog.config.configParser import URL, USR, PSWD, MODE, LOGBOOKS, TAGS, PROPERTIES, OWNER, PROP_ATT_DICT
from EXLog.epicsLogger.epicsLog import EpicsLogger

def createLogInstance(name):
    """
    Creates an Olog client, tags, logbooks, and properties specified by EXLog.conf./
    A series of configuration sets are available. configParser loads the default configuration.
    """
    logInstance = EpicsLogger()
    logInstance.createPythonLogger(name)
    logInstance.setOwner(owner=OWNER)
    if MODE == 'local':
        raise NotImplementedError("Local logging w/o remote Olog server will be implemented")
    else:
        logInstance.setLogMode(mode=MODE)
        new_log_mode = logInstance.get_LogMode()
        if new_log_mode != 'remote':
            raise ValueError('Invalid Logging Mode[remote/local]')
        logInstance.createOlogClient(name, URL, USR, PSWD)
        logInstance.populate()
        # logInstance.createMultipleLogbooks(LOGBOOKS, OWNER)
        # logInstance.createMultipleTags(TAGS)
        # logInstance.createMultipleProperties(PROP_ATT_DICT)
        return logInstance
