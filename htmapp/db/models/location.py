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
        database = get_db()