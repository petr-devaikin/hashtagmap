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

	lat_km = (msk.north - msk.south) / msk.height
	long_km = (msk.east - msk.west) / (msk.north_width + msk.south_width) * 2

	msk_coords = ((msk.north + msk.south) / 2, (msk.east + msk.west) / 2)

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
		print "+++ Moscow areas created {0} for latitude {1}, row {2}".format(counter, y, i)
		y -= lat_km * 2 * radius
		i += 1
