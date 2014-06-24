# -*- coding: utf-8 -*-
from peewee import *

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

    class Meta:
        database = db


class SimpleArea(Model):
    location = ForeignKeyField(Location, related_name='simple_areas')
    to_north = ForeignKeyField('self', related_name='to_south', null=True)
    to_west = ForeignKeyField('self', related_name='to_east', null=True)
    latitude = DoubleField()
    longitude = DoubleField()
    radius = IntegerField()
    updated = DateTimeField(null=True)

    def most_popular_tag(self):
        if self.hashtag_counts.count() > 0:
            return self.hashtag_counts.order_by(HashtagFrequency.count.desc()).get()
        else:
            return None


    def add_connections(self):
        all_north = SimpleArea.select().where((SimpleArea.longitude == self.longitude) & \
            (SimpleArea.latitude > self.latitude) & (SimpleArea.location == self.location))
        if all_north.count() > 0:
        	self.to_north = all_north.order_by(SimpleArea.latitude).get()

        all_west = SimpleArea.select().where((SimpleArea.latitude == self.latitude) & \
            (SimpleArea.longitude < self.longitude) & (SimpleArea.location == self.location))
        if all_west.count() > 0:
        	self.to_west = all_west.order_by(SimpleArea.longitude.desc()).get()

        self.save()


    class Meta:
        database = db


class Hashtag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class HashtagFrequency(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts')
    simple_area = ForeignKeyField(SimpleArea, related_name='hashtag_counts')
    count = IntegerField(default=0)

    class Meta:
        database = db
