# -*- coding: utf-8 -*-
from models import *

"""drop tables"""

if Location.table_exists():
	Location.drop_table()
	print '-- Location table dropped'

if SimpleArea.table_exists():
	SimpleArea.drop_table()
	print '-- SimpleArea table dropped'

if Hashtag.table_exists():
	Hashtag.drop_table()
	print '-- Hashtag table dropped'

if HashtagFrequency.table_exists():
	HashtagFrequency.drop_table()
	print '-- HashtagFrequency table dropped'


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
Location.create(name=u'Moscow', \
	north=55.996804, south=55.492144, west=37.235253, east=37.945527, \
	height=56132, north_width=44181, south_width=44756)
print "+++ Moscow location created"