'''
Created on Mar 28, 2014

@author: arkilic
'''

class Scan():
    """
    Provides a generic scan class
    """
    def __init__(self):
        """
        Constructor
        """
        self.__scan_id = None
        self.__PV_list = list()
        self.__epics_timestamp = None
    
    def scanId(self, id=None):
        if id is None:
            return self.scan_id
        else:
            self.__scan_id = id
    
    
    
        
        
        
        
        
class ascan(Scan):
    def setup_scan(self):
        pass
    
    def run_scan(self):
        pass
    
    def log_scan(self):
        pass
     
    
a = ascan()
print a.__scan_id