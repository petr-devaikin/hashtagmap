# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from peewee import *
from htmapp.db.models.db_engine import get_db

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

    def calc_most_popular_tag(self, ignore=[]):
        sq = self.hashtag_counts_sum.join(Hashtag)
        where = sq.where(~(Hashtag.name << ignore)).order_by(HashtagFrequencySum.count.desc())
        tag = where.first()
        if tag == None:
            self.most_popular_tag_name = None
            self.most_popular_tag_count = None
        else:
            self.most_popular_tag_name = tag.hashtag.name
            self.most_popular_tag_count = tag.count
        self.save()

    def count_of_tag(self, tag):
        sq = self.hashtag_counts_sum.join(Hashtag).where(Hashtag.name == tag)

        h = sq.first()
        if h == None:
            return 0
        else:
            return sq.first().count

    class Meta:
        database = get_db()