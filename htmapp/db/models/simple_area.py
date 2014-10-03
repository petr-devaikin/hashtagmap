# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from htmapp.db.models.hashtag import Hashtag
from peewee import *
from htmapp.db.db_engine import get_db

db = MySQLDatabase(None, threadlocals=True)

class SimpleArea(Model):
    location = ForeignKeyField(Location, related_name='simple_areas')
    column = IntegerField()
    row = IntegerField()
    most_popular_tag_name = CharField(null=True)
    most_popular_tag_count = IntegerField(null=True)
    latitude = DoubleField()
    longitude = DoubleField()
    radius = IntegerField()

    def count_of_tag(self, tag):
        sq = self.hashtag_counts_sum.join(Hashtag).where(Hashtag.name == tag)
        h = sq.first()
        return sq.first().count if h else 0

    class Meta:
        database = get_db()