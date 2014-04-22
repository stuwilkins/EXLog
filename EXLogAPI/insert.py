__author__ = 'arkilic'
"""
Provides tools to create a log entry
"""
from EXLogAPI.session_init import client

#TODO: Inside session, define a default configuration file
#TODO: Inside session, define default logbooks, tags, owner etc...


def capture(property_name, **kwds):
    """
    capture is used in order to capture name-value pairs:
        capture(property_name, attribute1=value1, attribute2=value2,...)
    It is important to understand capture does not create a log entry. It is only a simple buffer mechanism. In order to/
    create log entries with the name value pairs to be recorded, one has to first capture name value pairs in this/
    fashion then use log().
    """
    client.capture(property_name, **kwds)


def log(description, owner=None, logbooks=[], tags=[], attachments=[]):
    """
    Provides means to create log entries with captured name-value pairs. Creating a sample log entry:
        capture(property_name, attribute1=value1, attribute2=value2,...)
        log(description=sample_log, logbooks=["myLogbook"], tags=["myTag"], attachments="myThumbnail"])
    """
    client.log(description, owner, logbooks, tags, attachments)
