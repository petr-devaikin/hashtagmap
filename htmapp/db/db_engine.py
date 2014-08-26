# -*- coding: utf-8 -*-
from peewee import *

_db = Proxy()

def init_db(app):
    if app.config['DATABASE']['ENGINE'] == 'Sqlite':
        database = SqliteDatabase(app.config['DATABASE']['NAME'], threadlocals=True,
            **app.config['DATABASE']['PARAMS'])
    elif app.config['DATABASE']['ENGINE'] == 'MySQL':
        database = MySQLDatabase(app.config['DATABASE']['NAME'], threadlocals=True,
            **app.config['DATABASE']['PARAMS'])
    elif app.config['DATABASE']['ENGINE'] == 'Postgresql':
        database = PostgresqlDatabase(app.config['DATABASE']['NAME'], threadlocals=True,
            **app.config['DATABASE']['PARAMS'])
    else:
        raise Exception('Unknown database engine')

    _db.initialize(database)

def get_db():
    return _db