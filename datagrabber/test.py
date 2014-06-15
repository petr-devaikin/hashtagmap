# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.helper import datetime_to_timestamp
import time
import operator

def calc_tags(media):
	tags = {}
	for m in media:
		try:
			for t in m.tags:
				if t.name not in (u"moscow", u"москва"):
					if not t.name in tags:
						tags[t.name] = 1
					else:
						tags[t.name] += 1
		except AttributeError:
			pass
	"""print tags"""
	return tags

client_id = "fd2526cfad7d4aaa948d20314b938132"
client_secret = "348777df18ea4fceb1df573528757bb0"
moscow_coords = [55.7522200, 37.6155600]
distance = 5000

api = InstagramAPI(client_id=client_id, client_secret=client_secret)

max_stamp = time.time()

for i in range(1, 10):
	media = api.media_search(lat=moscow_coords[0], lng=moscow_coords[1], \
		distance=distance, max_timestamp=max_stamp, count=100)

	min_stamp = datetime_to_timestamp(media[-1].created_time)
	max_stamp = datetime_to_timestamp(media[0].created_time)
	print "{0} - {1}".format(min_stamp, max_stamp)

	tags = calc_tags(media)
	max_tag = max(tags.iteritems(), key=operator.itemgetter(1))[0]
	print "{0}: {1}".format(max_tag.encode('utf-8'), tags[max_tag])

	max_stamp = min_stamp


