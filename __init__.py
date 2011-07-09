#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'p0123n'

from os     import path
myPath = path.abspath(path.dirname(__file__))

import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open('%s/mybases.conf'%myPath))

from mygate import MyGate

# You can switch 'localhost' to any
# other mostly used data base.
def init(server = 'localhost'):
    params = dict()

    params['addr'] = str(config.get(server, 'addr'))
    params['port'] = int(config.get(server, 'port'))
    params['user'] = str(config.get(server, 'user'))
    params['pass'] = str(config.get(server, 'pass'))
    params['name'] = str(config.get(server, 'name'))

    return MyGate(params)

if __name__ == '__main__':
    gate = init()
    print gate.query('select version()')
