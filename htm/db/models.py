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
    updated = DateTimeField(null=True)

    def clear_old_hours(self, min_time):
        hours_to_clear = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << self.simple_areas, 
            TagsOfAreaInHour.max_stamp < min_time)
        count = hours_to_clear.count()

        HashtagFrequency.delete().where(HashtagFrequency.area_in_hour << hours_to_clear).execute()
        TagsOfAreaInHour.delete().where(TagsOfAreaInHour.area << self.simple_areas, 
            TagsOfAreaInHour.max_stamp < min_time).execute()

        print "Location {0}: {1} old hours to removed".format(self.name, count)

    def update_time(self):
        all_hours = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << self.simple_areas).order_by(TagsOfAreaInHour.max_stamp.desc())
        if all_hours.count() == 0:
            self.updated = None
        else:
            self.updated = all_hours.first().max_stamp
        self.save()

    class Meta:
        database = db


class IgnoreForLocation(Model):
    tag = CharField()
    location = ForeignKeyField(Location, related_name='ignore_list')

    class Meta:
        database = db


class Hashtag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class SimpleArea(Model):
    location = ForeignKeyField(Location, related_name='simple_areas')
    to_north = ForeignKeyField('self', related_name='to_south', null=True)
    to_west = ForeignKeyField('self', related_name='to_east', null=True)
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


class TagsOfAreaInHour(Model):
    area = ForeignKeyField(SimpleArea, related_name='tags_in_hour')
    max_stamp = DateTimeField()
    min_stamp = DateTimeField()
    processed = DateTimeField()

    class Meta:
        database = db


class HashtagFrequencySum(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts_sum')
    area = ForeignKeyField(SimpleArea, related_name='hashtag_counts_sum')
    count = IntegerField(default=0)

    class Meta:
        database = db


class HashtagFrequency(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts')
    area_in_hour = ForeignKeyField(TagsOfAreaInHour, related_name='hashtag_counts')
    count = IntegerField(default=0)

    class Meta:
        database = db
