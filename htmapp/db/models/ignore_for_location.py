# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from peewee import *
from htmapp.db.db_engine import get_db

db = MySQLDatabase(None, threadlocals=True)

class IgnoreForLocation(Model):
    tag = CharField()
    location = ForeignKeyField(Location, related_name='ignore_list')

    class Meta:
        database = get_db()