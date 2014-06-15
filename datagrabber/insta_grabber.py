# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.helper import datetime_to_timestamp
import operator

class InstaGrabber:
	MAX_SEARCH_COUNT = 100


	def __init__(self, client_id, client_secret):
		self.__api = InstagramAPI(client_id=client_id, client_secret=client_secret)


	def find_tags(self, coords, distance, max_date, min_date):
		tags = {}
		max_stamp = max_date
		last_id = -1
		while max_stamp > min_date:
			print "{0} -> {1}".format(max_stamp, min_date)

			media = self.__api.media_search(lat=coords[0], lng=coords[1], distance=distance, \
				max_timestamp=max_stamp, count=self.MAX_SEARCH_COUNT)

			last_id = media[-1]
			max_stamp = datetime_to_timestamp(media[-1].created_time)

			tags = {}
			self.__cals_tags(tags, media)
			max_tag = max(tags.iteritems(), key=operator.itemgetter(1))[0]
			print "{0}: {1}".format(max_tag.encode('utf-8'), tags[max_tag])


	def __cals_tags(self, tags, media):
		for m in media:
			try:
				for t in m.tags:
					"""if t.name not in (u"moscow", u"москва"):"""
					if not t.name in tags:
						tags[t.name] = 1
					else:
						tags[t.name] += 1
			except AttributeError:
				pass
