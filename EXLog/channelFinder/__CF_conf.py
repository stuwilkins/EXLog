'''
Created on Mar 31, 2014

@author: arkilic
'''
from EXLog.config._conf import _conf

channel_finder_config = {"URL" :_conf.get('channel_finder', 'url'),
                         "USR" : _conf.get('channel_finder', 'user'),
                         "PSWD" : _conf.get('channel_finder', 'password')}

