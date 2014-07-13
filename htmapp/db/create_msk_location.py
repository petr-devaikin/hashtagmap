# -*- coding: utf-8 -*-
from htmapp.db.models import *

def create_msk_location():
	msk = Location.create(name=u'Moscow', \
		north=55.996804, south=55.492144, west=37.235253, east=37.945527, \
		height=56132, north_width=44181, south_width=44756)
	print "+++ Moscow location created"


	for tag in [u'moscow', u'москва', u'russia', u'россия', u'vscorussia', u'vscomoscow', \
			u'msk', u'мск']:
		IgnoreForLocation.create(location=msk, tag=tag)


	radius = 500

	lat_km = (msk.north - msk.south) / msk.height * 1000
	long_km = (msk.east - msk.west) / (msk.north_width + msk.south_width) * 2 * 1000

	msk_coords = ((msk.north + msk.south) / 2, (msk.east + msk.west) / 2)

	y = msk_coords[0]
	while y > msk.south:
		x = msk_coords[1]
		counter = 0
		first_area = None
		last_area = None
		while x > msk.west:
			first_area = SimpleArea.create(location=msk, latitude=y, longitude=x, radius=radius)
			counter += 1
			x -= long_km * 2 * radius / 1000
		x = msk_coords[1] + long_km
		while x < msk.east:
			last_area = SimpleArea.create(location=msk, latitude=y, longitude=x, radius=radius)
			counter += 1
			x += long_km * 2 * radius / 1000
		print "+++ Moscow areas created {4}: ({0}, {1}) - ({2}, {3})".format(first_area.latitude, \
			first_area.longitude, last_area.latitude, last_area.longitude, counter)
		y -= lat_km

	y = msk_coords[0] + lat_km
	while y < msk.north:
		x = msk_coords[1]
		counter = 0
		first_area = None
		last_area = None
		while x > msk.west:
			first_area = SimpleArea.create(location=msk, latitude=y, longitude=x, radius=radius)
			counter += 1
			x -= long_km * 2 * radius / 1000
		x = msk_coords[1] + long_km
		while x < msk.east:
			last_area = SimpleArea.create(location=msk, latitude=y, longitude=x, radius=radius)
			counter += 1
			x += long_km * 2 * radius / 1000
		print "+++ Moscow areas created {4}: ({0}, {1}) - ({2}, {3})".format(first_area.latitude, \
			first_area.longitude, last_area.latitude, last_area.longitude, counter)
		y += lat_km