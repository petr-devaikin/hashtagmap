# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from htmapp.db.models.ignore_for_location import IgnoreForLocation
from htmapp.db.models.simple_area import SimpleArea
from htmapp.logger import get_logger
from flask import current_app

def create_london_location():
    if current_app.config['TESTING']:
        london = Location.create(name=u'London',
            north=51.709035, south=51.249583, west=-0.552444, east=0.305863,
            height=2000, north_width=4000, south_width=4500,
            timezone='Europe/London')
    else:
        london = Location.create(name=u'London',
            north=51.709035, south=51.249583, west=-0.552444, east=0.305863,
            height=51108, north_width=59328, south_width=59927,
            timezone='Europe/London')
    get_logger().info('London location created')

    for tag in [u'london']:
        IgnoreForLocation.create(location=london, tag=tag)


    radius = 500

    lat_km = london.lat_km()
    long_km = london.long_km()

    london_coords = (london.latitude(), london.longitude())

    y = london.north - lat_km * radius
    i = 0
    while y - lat_km * radius >= london.south:
        j = 0
        x = london.west + long_km * radius
        counter = 0
        while x + long_km * radius <= london.east:
            last_area = SimpleArea.create(location=london, latitude=y, longitude=x, radius=radius, row=i, column=j)
            counter += 1
            x += long_km * 2 * radius
            j += 1
        get_logger().debug("London areas created {0} for latitude {1}, row {2}".format(counter, y, i))
        y -= lat_km * 2 * radius
        i += 1
