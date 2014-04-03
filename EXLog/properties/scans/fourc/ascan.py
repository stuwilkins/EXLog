__author__ = 'arkilic'
from EXLog.properties.s.Scan import Scan
#TODO: Descriptor should be required once agreed on design
#TODO: Enforce data type and format on instance attributes

class ascan(Scan):
    """
    Usage: ascan motor_name start_pos end_pos interval time
    """
    def __init__(self, scan_id, motor_name, start_pos, end_pos, interval,
                 start_timestamp=None, end_timestamp=None, descriptor=None, geometry='fourc'):
        """
        Constructor
        """
        Scan.__init__(self, scan_id, start_timestamp, end_timestamp,descriptor)
        self.motor_name = motor_name
        self.geometry = 'fourc'

    def motor(self, motor_name=None):
        """
        Sets/returns the name of the motor for ascan instance
        """
        if motor_name is None:
            return self.motor_name
        else:
            self.motor_name = motor_name

    def start(self, time_stamp=None):
        if time_stamp is None:
            return self.start_timestamp
        else:
            self.start_timestamp = time_stamp

    def final(self, time_stamp=None):
        if time_stamp is None:
            return self.start_timestamp
        else:
            self.end_timestamp = time_stamp






#
#
# a = ascan(1,'delta', 1, 3, 134, 31)
# print a.scan_id
# print a.motor(motor_name='sigma')
# print a.motor()
# a.start(12)
# print a.start()