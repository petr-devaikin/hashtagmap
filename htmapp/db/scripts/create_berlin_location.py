# -*- coding: utf-8 -*-
from ..models.location import Location
from ..models.ignore_for_location import IgnoreForLocation
from ..models.simple_area import SimpleArea
from htmapp.logger import get_logger
from flask import current_app

def create_berlin_location():
    berlin = Location.create(name=u'Berlin',
        north=52.677519, south=52.337324, west=13.086277, east=13.763996,
        height=37840, north_width=45882, south_width=45882,
        timezone='Europe/Berlin')
    get_logger().info('Berlin location created')

    for tag in [u'berlin', u'vscoberlin', u'germany']:
        IgnoreForLocation.create(location=berlin, tag=tag)


    radius = 500

    lat_km = berlin.lat_km()
    long_km = berlin.long_km()

    london_coords = (berlin.latitude(), berlin.longitude())

    y = berlin.north - lat_km * radius
    i = 0
    while y - lat_km * radius >= berlin.south:
        j = 0
        x = berlin.west + long_km * radius
        counter = 0
        while x + long_km * radius <= berlin.east:
            last_area = SimpleArea.create(location=berlin, latitude=y, longitude=x, radius=radius, row=i, column=j)
            counter += 1
            x += long_km * 2 * radius
            j += 1
        get_logger().debug("Berlin areas created {0} for latitude {1}, row {2}".format(counter, y, i))
        y -= lat_km * 2 * radius
        i += 1
