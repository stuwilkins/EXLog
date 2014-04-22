__author__ = 'arkilic'
"""
Provides routines in order to create Olog Properties(Attributes-Values), Logbooks, and Tags
"""
from EXLogAPI.session_init import client


def create_properties(property_name, attributes):
    """
    Creates a property given property_name and list of attributes. Properties are used in order to name a specific/
    process, experiment, and/or custom notes. Properties contain attributes that are name-value pairs.
    """
    return_status = client.createProperty(property_name, attributes)
    if return_status is False:
        result = 'Property creation failed'
    else:
        result = 'Property with given attributes created/updated'
    return result


def create_logbook(logbook_name, **kwargs):
    """
    Creates a custom logbook that is used to contain log entries. Owner is read from EXLog.conf configuration file/
    however, it can also be specified as an argument to this routine create_logbook(logbook_name=..., owner=...).
    """
    return_status = client.createLogbook(logbook_name, **kwargs)
    result = return_status
    if return_status is None:
        result = 'Logbook created'
    return result


def create_tag(tag_name):
    """
    Creates custom tag that can be used to differentiate and/or specify a set of log entries. Tags, just like logbooks,/
    are queryable. EXLogAPI.retrieve.query(tag='my_tag') will return all log entries in all the logbooks (unless logbook/
    is specified) with tag='my_tag'.
    """
    return_status = client.createTag(tag_name)
    result = return_status
    if return_status is None:
        result = 'Tag created'
    return result


