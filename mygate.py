#! /usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'p0123n'

import MySQLdb
from   MySQLdb import cursors

def keepSingleConn(cls):
    instances = dict()
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getInstance

@keepSingleConn
class Connection():
    def __init__(self):
        self.connection = None
        self.cursor     = None

    def connect(self, params):
        connection = MySQLdb.connect(
            host        = params['addr'],
            port        = params['port'],
            user        = params['user'],
            passwd      = params['pass'],
            db          = params['name'],
            cursorclass = params['curs']
        )
        self.cursor = connection.cursor()
        self.cursor.execute('set names utf8')
        self.cursor.execute('set session time_zone="%s"' % params['tmzn'])
        return connection, self.cursor

class Query():
    def __init__(self, params):
        params['curs'] = cursors.SSDictCursor
        self.connection, self.cursor = Connection().connect(params)

    def query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def __iter__(self):
        for row in self.connection:
            yield row

    def __enter__(self):
        return self.cursor

    def __ex_t__(self,ext_type,exc_value,traceback):
        self.connection.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()


class Dump():
    def __init__(self, params):
        params['curs'] = cursors.SSCursor
        self.connection, self.cursor = Connection().connect(params)

    def dump(self, query, filn=None, dirn='.', sep=';', pref='mygate'):

        if not filn:
            from datetime import datetime
            filn = datetime.today().strftime('%Y-%m-%d(%H%M%S).csv')
            filn = '%s/%s_%s' % (dirn, pref, filn)
        else:
            filn = '%s/%s%s' % (dirn, pref, filn)

        fn = open(filn, 'w')

        self.cursor.execute(query)
        rows = 0

        for row in self.cursor:
            fn.write(sep.join( str(field) for field in row ) + '\n')
            rows += 1
        fn.close()

        return filn, rows

class MyGate():
    def __init__(self, params):
        self._query = None
        self._dump  = None
        self._params= params

    def query(self, *args, **kwargs):
        self._query = self._query or Query(self._params)
        return self._query.query(*args, **kwargs)

    def dump(self, *args, **kwargs):
        self._dump  = self._dump  or Dump(self._params)
        return self._dump.dump(*args, **kwargs)

if __name__ == '__main__':
    print 'Hi.'
