# -*- coding: utf-8 -*-
from peewee import *

_db = Proxy()

def init_db(app):
    if app.config['TESTING']:
        database = SqliteDatabase(app.config['TEST_DATABASE'], threadlocals=True)
    elif app.config['DEBUG']:
        database = MySQLDatabase(app.config['DB_NAME'],
            user=app.config['DB_USER'], password=app.config['DB_PASSWORD'], threadlocals=True)
    else:
        database = PostgresqlDatabase(app.config['DB_NAME'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            threadlocals=True)
    _db.initialize(database)

def get_db():
    return _db