# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from htmapp.db.models.ignore_for_location import IgnoreForLocation
from htmapp.db.models.simple_area import SimpleArea
from htmapp.logger import get_logger
from flask import current_app

def create_msk_location():
    if current_app.config['TESTING']:
        msk = Location.create(name=u'Moscow',
            north=55.996804, south=55.492144, west=37.235253, east=37.945527,
            height=3000, north_width=3000, south_width=3000,
            timezone='Europe/Moscow')
    else:
        msk = Location.create(name=u'Moscow',
            north=55.996804, south=55.492144, west=37.235253, east=37.945527,
            height=56132, north_width=44181, south_width=44756,
            timezone='Europe/Moscow')
    get_logger().info('Moscow location created')


    for tag in [u'moscow', u'москва', u'russia', u'россия', u'vscorussia', u'vscomoscow', u'vscomsk',
            u'msk', u'мск']:
        IgnoreForLocation.create(location=msk, tag=tag)


    radius = 500

    lat_km = msk.lat_km()
    long_km = msk.long_km()

    msk_coords = (msk.latitude(), msk.longitude())

    y = msk.north - lat_km * radius
    i = 0
    while y - lat_km * radius >= msk.south:
        j = 0
        x = msk.west + long_km * radius
        counter = 0
        while x + long_km * radius <= msk.east:
            last_area = SimpleArea.create(location=msk, latitude=y, longitude=x, radius=radius, row=i, column=j)
            counter += 1
            x += long_km * 2 * radius
            j += 1
        get_logger().info("Moscow areas created {0} for latitude {1}, row {2}".format(counter, y, i))
        y -= lat_km * 2 * radius
        i += 1
