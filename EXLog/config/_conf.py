__author__ = 'arkilic'

def __loadConfig():
    import os.path
    import ConfigParser
    dflt={'url':'http://localhost:8000/Olog'}
    cf=ConfigParser.SafeConfigParser(defaults=dflt)
    cf.read([
        '/etc/pyOlog.conf',
        os.path.expanduser('~/pyOlog.conf'),
        'pyOlog.conf'
    ])
    return cf

_conf=__loadConfig()