# -*- coding: utf-8 -*-
from models import *
from create_msk_location import *
from create_areas_connections import *

def drop_tables():
    if HashtagFrequency.table_exists():
        HashtagFrequency.drop_table()
        print '-- HashtagFrequency table dropped'

    if HashtagFrequencySum.table_exists():
        HashtagFrequencySum.drop_table()
        print '-- HashtagFrequencySum table dropped'
        
    if TagsOfAreaInHour.table_exists():
        TagsOfAreaInHour.drop_table()
        print '-- TagsOfAreaInHour table dropped'

    if SimpleArea.table_exists():
    	SimpleArea.drop_table()
    	print '-- SimpleArea table dropped'
        
    if IgnoreForLocation.table_exists():
        IgnoreForLocation.drop_table()
    print '-- IgnoreForLocation table dropped'

    if Location.table_exists():
    	Location.drop_table()
	print '-- Location table dropped'

    if Hashtag.table_exists():
        Hashtag.drop_table()
        print '-- Hashtag table dropped'


def create_tables():
    Location.create_table()
    print '++ Location table created'

    IgnoreForLocation.create_table()
    print '++ IgnoreForLocation table created'

    Hashtag.create_table()
    print '++ Hashtag table created'

    SimpleArea.create_table()
    print '++ SimpleArea table created'

    TagsOfAreaInHour.create_table()
    print '++ TagsOfAreaInHour table created'

    HashtagFrequency.create_table()
    print '++ HashtagFrequency table created'

    HashtagFrequencySum.create_table()
    print '++ HashtagFrequencySum table created'


def init_data():
    create_msk_location()
    create_areas_connections()
    

def init_database():
    drop_tables()
    create_tables()
    init_data()