# -*- coding: utf-8 -*-
from .models.hashtag_frequency import HashtagFrequency
from .models.tags_of_area_in_hour import TagsOfAreaInHour
from .models.simple_area import SimpleArea
from .models.ignore_for_location import IgnoreForLocation
from .models.location import Location
from .models.hashtag import Hashtag
from .models.area_group import AreaGroup
from htmapp.logger import get_logger
from .create_msk_location import *
from .create_london_location import *

def drop_tables():
    if HashtagFrequency.table_exists():
        HashtagFrequency.drop_table()
        get_logger().info('HashtagFrequency table dropped')
        
    if TagsOfAreaInHour.table_exists():
        TagsOfAreaInHour.drop_table()
        get_logger().info('TagsOfAreaInHour table dropped')

    if SimpleArea.table_exists():
    	SimpleArea.drop_table()
    	get_logger().info('SimpleArea table dropped')
        
    if IgnoreForLocation.table_exists():
        IgnoreForLocation.drop_table()
    get_logger().info('IgnoreForLocation table dropped')

    if AreaGroup.table_exists():
        AreaGroup.drop_table()
    get_logger().info('AreaGroup table dropped')

    if Location.table_exists():
        Location.drop_table()
    get_logger().info('Location table dropped')

    if Hashtag.table_exists():
        Hashtag.drop_table()
        get_logger().info('Hashtag table dropped')


def create_tables():
    Location.create_table()
    get_logger().info('Location table created')

    AreaGroup.create_table()
    get_logger().info('AreaGroup table created')

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


def init_data():
    create_msk_location()
    create_london_location()
    

def init_database():
    drop_tables()
    create_tables()
    init_data()