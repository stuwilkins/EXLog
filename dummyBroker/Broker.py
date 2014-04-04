__author__ = 'arkilic'
from EXLog.epicsLogger.smartLog import createLogInstance
from EXLog.propertyDepot.scans import *


class Broker():
    """
    A dummy data broker instance. Alongside configuration read into EXLog from configuration file, another set/
    of configuration files will be read using Broker's parser. (Maybe pass all configuration to this module?)

    """
    def __init__(self, session_name):
        try:
            self.exlog_client = createLogInstance(session_name)
        except:
            raise
        self.id = 0
        #Channelfinder client (if any) goes here
        #instruments can be controlled via another client
        #data broker uses 4 clients: EXLog, instrumentControl(?), channelfinder(?),
        #channel archiver. each client manages requests separately

    def increase_id(self):
        self.id += 1

    def create_property(self, property_name):
        if type(property_name) is list:
            for entry in property_name:
                if entry in scan_list:
                    property = scans[entry]
                    self.exlog_client.createProperty(entry, property['attributes'])
                else:
                    raise ValueError(str(entry) + 'property is not in the property template list')
    def capture(self,property_name,**kwds):
        #TODO: Add additional logic to capture() to avoid logging identical entries:all fields match perfectly
        #TODO: Ensure the scan_id has not been used before.

        self.exlog_client.capture(property_name, **kwds)

    def log(self,description, owner=None, logbooks=[], tags=[], attachments=[],):

        self.exlog_client.log(description,owner,logbooks,tags,attachments)

    def get_captured(self):
        captured_properties = self.exlog_client.get_buffered_properties()
        for entry in captured_properties:
            print entry.getName()
            print '\t', entry.getAttributes()





scan = Broker('arman')
scan.create_property(['ascan'])

# scan.exlog_client.createProperty('arman33',['scan_id', 'start_timestamp', 'end_timestamp', 'descriptor', 'start', 'final', 'interval', 'descriptor', 'geometry'])
# print scan.exlog_client.get_PropertyWithAttributes()['arman33']

scan.capture('ascan',scan_id=0)
scan.capture('ascan',scan_id=1)
scan.get_captured()
logbook = scan.exlog_client.get_Logbooks()[0]
scan.log(description='first log attempt using dummyBroker',logbooks=[logbook])

