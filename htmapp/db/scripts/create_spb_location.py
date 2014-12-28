# -*- coding: utf-8 -*-
from ..models.location import Location
from ..models.ignore_for_location import IgnoreForLocation
from ..models.simple_area import SimpleArea
from htmapp.logger import get_logger
from flask import current_app

def create_spb_location():
    spb = Location.create(name=u'Saint Petersburg',
        north=60.091486, south=59.744044, west=30.089023, east=30.562465,
        height=38646, north_width=26396, south_width=26396,
        timezone='Europe/Moscow')
    get_logger().info('Saint Petersburg location created')

    for tag in [u'spb', u'питер', u'saintpetersburg', u'петербург', u'спб', u'vscospb', u'vscorussia', u'russia']:
        IgnoreForLocation.create(location=spb, tag=tag)


    radius = 500

    lat_km = spb.lat_km()
    long_km = spb.long_km()

    london_coords = (spb.latitude(), spb.longitude())

    y = spb.north - lat_km * radius
    i = 0
    while y - lat_km * radius >= spb.south:
        j = 0
        x = spb.west + long_km * radius
        counter = 0
        while x + long_km * radius <= spb.east:
            last_area = SimpleArea.create(location=spb, latitude=y, longitude=x, radius=radius, row=i, column=j)
            counter += 1
            x += long_km * 2 * radius
            j += 1
        get_logger().debug("Saint Petersburg areas created {0} for latitude {1}, row {2}".format(counter, y, i))
        y -= lat_km * 2 * radius
        i += 1
