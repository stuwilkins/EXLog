__author__ = 'arkilic'
from EXLog.epicsLogger.smartLog import createLogInstance
from EXLog.instrumentControl.scan.fourc.ascan import ascan


# client = createLogInstance('trial')
a = ascan(1,3,3,4,5,6)

