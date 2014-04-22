"""
Copyright (c) 2014 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.
Created on April 3, 2014

@author: Arman Arkilic
"""
__author__ = 'arkilic'

class Scan():
    """
    Scan class serves as a template for all s routines.
    """
    def __init__(self, id, start_timestamp=None, end_timestamp=None,descriptor=None):
        """
        Constructor
        """
        self.scan_id = id
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.descriptor = descriptor #epics process variables will be determined by parsing this descriptor
        #TODO:Clarify the use of descriptor (Config files + ChannelFinder) or Config Files+....

    def id(self, **args):
        """
        Assigns/returns scan_id for given s instance
        """
        #TODO: In the future add more id management mechanism. That is the reason behind using **args
        if len(args) == 0:
            return self.scan_id
        else:
            for entry in args.keys():
                if entry is 'scan_id':
                    self.scan_id = args['scan_id']
                else:
                    raise ValueError('Not a valid parameter')

    def timestamp(self):
        """
        Returns a dictionary of epics_timestamps for s instances
        Dictionary: {'start':value, 'end' : value}
        """
        return {'start' : self.start_timestamp, 'end' : self.end_timestamp}

    def __setTimeStamp(self, start, end=None):
        """
        Assigns s start and end times.Start time is required while end time depends on developer preference
        """
        self.start_timestamp = start
        self.end_timestamp = end

    def descriptor(self):
        raise NotImplementedError("Descriptor schema has to be discussed and agreed on")
