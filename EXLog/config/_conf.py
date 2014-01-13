__author__ = 'arkilic'

def __loadConfig():
    import os.path
    import ConfigParser
    cf=ConfigParser.SafeConfigParser()
    cf.read([
        '/etc/EXLog.conf',
        os.path.expanduser('~/EXLog.conf'),
        'EXLog.conf'
    ])
    return cf

_conf=__loadConfig()