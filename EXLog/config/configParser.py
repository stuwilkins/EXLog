"""
Copyright (c) 2014 Brookhaven National Laboratory
All rights reserved. Use is subject to license terms and conditions.
Created on Jan 13, 2014

@author: Arman Arkilic
"""
#TODO: During multiple tag, logbook, property parse make sure space after comma is enforced.

from EXLog.config._conf import _conf

configs = _conf.items('configs')

def compose_configuration_params(configs, config_key):
    """
    Returns the config file parameters to be consumed by epicsLogger routines in order to perform experimental logging.
    """
    configuration_parameters = None
    config_dict = __configuration_set_parser(configs)
    if config_dict.has_key(config_key):
        configuration_parameters = __configEncoder(config_key,config_dict)
    else:
        raise ValueError('Configuration ' + str(config_key) + ' does not exist')
    return configuration_parameters

def __configuration_set_parser(configs):
    config_dict = dict()
    for entry in configs:
        config_dict[entry[0]] = entry[1]
    return config_dict


def __configEncoder(config_name, config_dict):
    """
    Composes a dictionary of configuration parameters
    """
    config_params = dict()
    conf_set_name = config_dict[config_name]
    conf_set_params = list()
    for entry in _conf.items(conf_set_name):
        conf_set_params.append(entry[0])
    __verify_config_params(conf_set_params)
    try:
        config_params['url'] = _conf.get(conf_set_name, 'url')
        config_params['user'] = _conf.get(conf_set_name, 'user')
        config_params['password'] = _conf.get(conf_set_name, 'password')
        config_params['logging_mode'] = _conf.get(conf_set_name, 'logging_mode')
        config_params['logbooks'] = _conf.get(conf_set_name, 'logbooks')
        config_params['tags'] = _conf.get(conf_set_name, 'tags')
        config_params['properties'] = _conf.get(conf_set_name, 'properties')
        config_params['log_owner'] = _conf.get(conf_set_name, 'log_owner')
    except:
        raise
    return config_params

def __verify_config_params(config):
    """
    Verifies the configuration parameters
    """
    required_keys = ['url', 'user', 'password', 'logging_mode', 'logbooks', 'tags', 'properties', 'log_owner']
    keys = config
    __verify_required_fields(keys, required_keys)

def __verify_required_fields(keys, required_key_values):
    for entry in keys:
        if entry not in required_key_values:
            raise ValueError('Configuration file can not include required field ' + str(entry))
    for entry in required_key_values:
        if entry not in keys:
            raise ValueError('Configuration file is required to have ' + str(entry) + ' field')

def extractMultiple(temp_item):
    return temp_item.split(', ')

params = compose_configuration_params(configs,'config0')
temp_tags = params['tags']
temp_props = params['properties']
URL = params['url']
USR = params['user']
PSWD = params['password']
MODE = params['logging_mode']
LOGBOOKS = extractMultiple(params['logbooks'])
OWNER = params['log_owner']
temp_prop = params['properties']
TAGS = extractMultiple(params['tags'])
temp_prop = temp_prop.split(', ')
for entry in temp_prop:
    print entry.split(' ( ,) ')