# -*- coding: utf-8 -*-
from peewee import *
from htmapp.db.models.db_engine import get_db


db = MySQLDatabase(None, threadlocals=True)

class Location(Model):
    name = CharField()
    north = DoubleField()
    south = DoubleField()
    west = DoubleField()
    east = DoubleField()
    height = IntegerField()
    north_width = IntegerField()
    south_width = IntegerField()
    updated = DateTimeField(null=True)

    def latitude(self):
        return (self.north + self.south) / 2

    def longitude(self):
        return (self.west + self.east) / 2

    class Meta:
        database = get_db()