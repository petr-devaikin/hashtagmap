# -*- coding: utf-8 -*-
from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.simple_area import SimpleArea
from peewee import *
from htmapp.db.models.db_engine import get_db

db = MySQLDatabase(None, threadlocals=True)

class HashtagFrequencySum(Model):
    hashtag = ForeignKeyField(Hashtag, related_name='counts_sum')
    area = ForeignKeyField(SimpleArea, related_name='hashtag_counts_sum')
    count = IntegerField(default=0)

    class Meta:
        database = get_db()
