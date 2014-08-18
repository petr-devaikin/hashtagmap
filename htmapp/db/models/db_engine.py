# -*- coding: utf-8 -*-
from peewee import *

_db = MySQLDatabase(None, threadlocals=True)

def get_db():
    return _db