__author__ = 'arkilic'
"""
Provides tools to create a log entry
"""
from EXLogAPI.session_init import client
#TODO: Inside session, define a default configuration file
#TODO: Inside session, define default logbooks, tags, owner etc...
def capture(property_name, **kwds):
    client.capture(property_name, **kwds)

def log(description, owner=None, logbooks=[], tags=[], attachments=[]):
    client.log(description, owner, logbooks, tags, attachments)
