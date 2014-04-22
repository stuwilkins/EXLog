__author__ = 'arkilic'
"""
Provides routines in order to create Olog Properties(Attributes-Values), Logbooks, and Tags
"""
from EXLogAPI.session_init import client


def create_properties(property_name, attributes):
    return_status = client.createProperty(property_name, attributes)
    if return_status is False:
        result = 'Property creation failed'
    else:
        result = 'Property with given attributes created/updated'
    return result


def create_logbook(logbook_name, **kwargs):
    return_status = client.createLogbook(logbook_name, **kwargs)
    result = return_status
    if return_status is None:
        result = 'Logbook created'
    return result


def create_tag(tag_name):
    return_status = client.createTag(tag_name)
    result = return_status
    if return_status is None:
        result = 'Tag created'
    return result


