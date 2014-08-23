# -*- coding: utf-8 -*-
from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour
from htmapp.db.db_engine import get_db
from peewee import *

db = MySQLDatabase(None, threadlocals=True)


class HashtagFrequency(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts')
    area_in_hour = ForeignKeyField(TagsOfAreaInHour, related_name='hashtag_counts')
    count = IntegerField(default=0)

    class Meta:
        database = get_db()
        indexes = (
            (('hashtag', 'area_in_hour'), True),
        )
