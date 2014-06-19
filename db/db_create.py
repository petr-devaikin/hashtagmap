# -*- coding: utf-8 -*-
from models import *
from db_create_msk_location import *

db.init('hashtag_map', user='hashtag', password='123')

"""drop tables"""

if HashtagFrequency.table_exists():
	HashtagFrequency.drop_table()
	print '-- HashtagFrequency table dropped'

if Hashtag.table_exists():
	Hashtag.drop_table()
	print '-- Hashtag table dropped'

if SimpleArea.table_exists():
	SimpleArea.drop_table()
	print '-- SimpleArea table dropped'

if Location.table_exists():
	Location.drop_table()
	print '-- Location table dropped'


"""create tables"""

Location.create_table()
print '++ Location table created'

SimpleArea.create_table()
print '++ SimpleArea table created'

Hashtag.create_table()
print '++ Hashtag table created'

HashtagFrequency.create_table()
print '++ HashtagFrequency table created'


"""init data"""
create_msk_location()