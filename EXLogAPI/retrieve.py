__author__ = 'arkilic'
"""
Provides simple interface to query Olog Database
"""
from EXLogAPI.session_init import client


def query(**kwds):
    return client.find(**kwds)
