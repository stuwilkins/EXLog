__author__ = 'arkilic'
from EXLog.epicsLogger.smartLog import createLogInstance
"""
Session information is parsed in configParser used in creation of createLogInstance
"""
#TODO: Make session_init smart enough to return clients and import libraries based on access mode provided by config file
#TODO: Read client name from config file

client = createLogInstance('default')

