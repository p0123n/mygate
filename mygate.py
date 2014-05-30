#-*- coding:utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

""" Another one lightweight wrapper around MySQLdb.
"""

try:
    import MySQLdb
    from   MySQLdb import cursors
except ImportError:
    raise

VERSION = "3.0.0"
VERSION_INFO = (3, 0, 0, 0)

def new(cls, *args, **kwargs):
    return Query(*args, **kwargs)

def keep_single_conn(cls):
    """ Single connection
    """
    instances = dict()
    def get_instance():
        """ instances
        """
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance

@keep_single_conn
class Connection(object):
    """ MySQL connection init
    """
    def __init__(self):
        self.connection = None
        self.cursor = None

    @staticmethod
    def get_connection(params):
        """ MySQL connection init
        """
        return MySQLdb.connect(
            host=params['addr'],
            port=params['port'],
            user=params['user'],
            passwd=params['pass'],
            db=params['name'],
            cursorclass=params['curs']
        )

    def connect(self, params):
        """ MySQL connection init
        """
        self.cursor = self.get_connection(params).cursor()
        self.cursor.execute('set names utf8')
        self.cursor.execute('set session time_zone="%s"' % params['tmzn'])
        return self.get_connection(params), self.cursor

class Query(object):
    """ Only for small datasets
    """
    def __init__(self, params):
        params['curs'] = cursors.SSDictCursor
        self.connection, self.cursor = Connection().connect(params)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Query'

    def query(self, query):
        """ Only for small datasets
        """
        try:
            self.cursor.execute(query)
            __buffer = []
            for row in self.cursor:
                __buffer.append(row)
            return __buffer
        finally:
            self.cursor.close()

    def __iter__(self):
        for row in self.cursor:
            yield row

    def __enter__(self):
        return self.cursor

class Dump(object):
    """ Only for huge datasets
    """
    def __init__(self, params):
        params['curs'] = cursors.SSCursor
        self.connection, self.cursor = Connection().connect(params)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Dump'

    def dump(self, query, options):
        """ Only for huge datasets
        """

        if 'dirname' not in options:
            options['dirname'] = '.'

        if 'separator' not in options:
            options['separator'] = ';'

        if 'file_prefix' not in options:
            options['file_prefix'] = 'mgdump_'

        if 'filename' not in options:
            from datetime import datetime
            __datetime = datetime.today().strftime('%Y-%m-%d(%H%M%S)')
            options['filename'] = __datetime + '.csv'
            options['filename'] = '%s/%s_%s' % (
                options['dirname'],
                options['file_prefix'],
                options['filename']
            )
        else:
            options['filename'] = '%s/%s%s' % (
                options['dirname'],
                options['file_prefix'],
                options['filename']
            )

        __filename = open(options['filename'], 'w')

        self.cursor.execute(query)
        rows = 0

        for row in self.cursor:
            __filename.write(
                options['separator'].join(str(field) for field in row) + '\n'
            )
            rows += 1
        __filename.close()

        return options['filename'], rows

class MyGate(object):
    """ Main class
    """

    actions = {}

    def __init__(self, params):
        self._query = None
        self._dump = None
        self._params = params

    def __getattr__(self, action, *args, **kwargs):
        def function(params):
            """function"""
            if action not in self.actions:
                self.actions[action] = new(action.title(), self._params)
            method = getattr(self.actions[action], action)
            return method(params)
        return function

if __name__ == '__main__':
    print 'Hi.'
