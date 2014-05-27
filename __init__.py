#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Another one lightweight wrapper around MySQLdb.
"""

from os import path
MYPATH = path.abspath(path.dirname(__file__))

import ConfigParser
CONFIG = ConfigParser.ConfigParser()
CONFIG.readfp(open('%s/mybases.conf' % MYPATH))

from mygate import MyGate

# You can switch 'localhost' to any
# other mostly used data base.
def init(server='localhost'):
    """Loads config
    """
    params = dict()

    params['addr'] = str(CONFIG.get(server, 'addr'))
    params['port'] = int(CONFIG.get(server, 'port'))
    params['user'] = str(CONFIG.get(server, 'user'))
    params['pass'] = str(CONFIG.get(server, 'pass'))
    params['name'] = str(CONFIG.get(server, 'name'))
    params['tmzn'] = str(CONFIG.get(server, 'tmzn'))

    return MyGate(params)

if __name__ == '__main__':
    GATE = init()
    print GATE.query('select version()')
