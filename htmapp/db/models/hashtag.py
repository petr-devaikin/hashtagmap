# -*- coding: utf-8 -*-
from htmapp.db.db_engine import get_db
from peewee import *

class Hashtag(Model):
    name = CharField(unique=True)

    class Meta:
        database = get_db()