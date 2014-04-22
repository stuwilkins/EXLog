__author__ = 'arkilic'
"""
Provides simple interface to query Olog Database
"""
from EXLogAPI.session_init import client


def query(**kwds):
    """
     Search for logEntries based on one or many search criteria
        >> find(search='*Timing*')
        query logentries with the text Timing in the description

        >> query(tag='magnets')
        find log entries with the a tag named 'magnets'

        >> query(logbook='controls')
        find log entries in the logbook named 'controls'

        >> query(property='context')
        find log entires with property named 'context'

        >> query(start=str(time.time() - 3600)
        find the log entries made in the last hour
        >> find(start=123243434, end=123244434)
        find all the log entries made between the epoc times 123243434 and 123244434

        Searching using multiple criteria
        >>query(logbook='contorls', tag='magnets')
        find all the log entries in logbook 'controls' AND with tag named 'magnets'
    """
    return client.find(**kwds)
