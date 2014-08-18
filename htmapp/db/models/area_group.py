# -*- coding: utf-8 -*-
from htmapp.db.models.db_engine import get_db
from htmapp.db.models.location import Location
from peewee import *

class AreaGroup(Model):
    location = ForeignKeyField(Location, related_name='area_groups')
    tag = CharField()
    count = IntegerField()
    areas_count = IntegerField()
    north = DoubleField()
    south = DoubleField()
    west = DoubleField()
    east = DoubleField()
    radius = IntegerField()

    def normal_count(self):
        return int(float(self.count) / self.areas_count)

    class Meta:
        database = get_db()