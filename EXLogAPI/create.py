__author__ = 'arkilic'
"""
Provides routines in order to create Olog Properties(Attributes-Values), Logbooks, and Tags
"""
from EXLog.epicsLogger.smartLog import createLogInstance

#TODO: Read client name from config file

client = createLogInstance('default')

def create_properties(property_name, attributes):
    client.createProperty(property_name, attributes)


def create_logbook(logbook_name, **kwargs):
    client.createLogbook(logbook_name, **kwargs)


def create_tag(tag_name):
    client.createTag(tag_name)


