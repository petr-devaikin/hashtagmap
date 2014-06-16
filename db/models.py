# -*- coding: utf-8 -*-
from peewee import *

db = SqliteDatabase('tags.db')

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
	latitude = DoubleField()
	longitude = DoubleField()
	radius = IntegerField()
	updated = DateTimeField(null=True)

	class Meta:
		database = db


class Hashtag(Model):
	name = CharField()

	class Meta:
		database = db


class HashtagFrequency(Model):
	hashtag = ForeignKeyField(Hashtag, related_name='counts')
	simple_area = ForeignKeyField(SimpleArea, related_name='hashtag_counts')

	class Meta:
		database = db
