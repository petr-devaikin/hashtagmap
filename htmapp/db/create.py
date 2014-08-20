# -*- coding: utf-8 -*-
from htmapp.db.models import *
from htmapp.logger import get_logger

def drop_tables():
    if HashtagFrequency.table_exists():
        HashtagFrequency.drop_table()
        get_logger().info('HashtagFrequency table dropped')

    if HashtagFrequencySum.table_exists():
        HashtagFrequencySum.drop_table()
        get_logger().info('HashtagFrequencySum table dropped')
        
    if TagsOfAreaInHour.table_exists():
        TagsOfAreaInHour.drop_table()
        get_logger().info('TagsOfAreaInHour table dropped')

    if SimpleArea.table_exists():
    	SimpleArea.drop_table()
    	get_logger().info('SimpleArea table dropped')
        
    if IgnoreForLocation.table_exists():
        IgnoreForLocation.drop_table()
    get_logger().info('IgnoreForLocation table dropped')

    if Location.table_exists():
    	Location.drop_table()
	get_logger().info('Location table dropped')

    if Hashtag.table_exists():
        Hashtag.drop_table()
        get_logger().info('Hashtag table dropped')


def create_tables():
    Location.create_table()
    get_logger().info('Location table created')

    IgnoreForLocation.create_table()
    get_logger().info('IgnoreForLocation table created')

    Hashtag.create_table()
    get_logger().info('Hashtag table created')

    SimpleArea.create_table()
    get_logger().info('SimpleArea table created')

    TagsOfAreaInHour.create_table()
    get_logger().info('TagsOfAreaInHour table created')

    HashtagFrequency.create_table()
    get_logger().info('HashtagFrequency table created')

    HashtagFrequencySum.create_table()
    get_logger().info('HashtagFrequencySum table created')


def init_data():
    from create_msk_location import *
    from create_london_location import *

    create_msk_location()
    create_london_location()
    

def init_database():
    drop_tables()
    create_tables()
    init_data()