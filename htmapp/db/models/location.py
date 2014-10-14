# -*- coding: utf-8 -*-
from peewee import *
from htmapp.db.db_engine import get_db
import pytz


db = MySQLDatabase(None, threadlocals=True)

class Location(Model):
    name = CharField(unique=True)
    north = DoubleField()
    south = DoubleField()
    west = DoubleField()
    east = DoubleField()
    height = IntegerField()
    north_width = IntegerField()
    south_width = IntegerField()
    timezone = CharField()
    updated = DateTimeField(null=True)

    def latitude(self):
        return (self.north + self.south) / 2

    def longitude(self):
        return (self.west + self.east) / 2

    def lat_km(self):
        return (self.north - self.south) / self.height

    def long_km(self):
        return (self.east - self.west) / (self.north_width + self.south_width) * 2

    def pretty_updated(self):
        if self.updated:
            updated_time = self.updated.replace(tzinfo=pytz.timezone('GMT'))
            return updated_time.astimezone(pytz.timezone(self.timezone)).replace(tzinfo=None)
        else:
            return ''

    class Meta:
        database = get_db()