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


class SimpleArea(Model):
    location = ForeignKeyField(Location, related_name='simple_areas')
    to_north = ForeignKeyField('self', related_name='to_south', null=True)
    to_west = ForeignKeyField('self', related_name='to_east', null=True)
    latitude = DoubleField()
    longitude = DoubleField()
    radius = IntegerField()

    def most_popular_tag(self):
        if not hasattr(self, '__most_popular_tag__'):
            if self.tags_in_hour.count() > 0:
                count_sum = fn.Sum(HashtagFrequency.count)

                sq = Hashtag.select(Hashtag, count_sum.alias('count_sum'))
                join = sq.join(HashtagFrequency).join(TagsOfAreaInHour)
                where = join.where(TagsOfAreaInHour.area << self.tags_in_hour)
                group = where.group_by(Hashtag).order_by(count_sum.desc())

                self.__most_popular_tag__ = group.first()
            else:
                self.__most_popular_tag__ = None
        return self.__most_popular_tag__

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


class Hashtag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db


class HashtagFrequency(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts')
    area_in_hour = ForeignKeyField(TagsOfAreaInHour, related_name='hashtag_counts')
    count = IntegerField(default=0)

    class Meta:
        database = db
