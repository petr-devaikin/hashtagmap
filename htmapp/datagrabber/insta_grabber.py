# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.helper import datetime_to_timestamp
import operator

class InstaGrabber:
    MAX_SEARCH_COUNT = 100

    def __init__(self, client_id, client_secret):
        self.__api = InstagramAPI(client_id=client_id, client_secret=client_secret)


    def find_tags(self, coords, distance, max_date, min_date, ignore_list=[]):
        tags = {}
        max_stamp = max_date
        while max_stamp > min_date:
            print "Request for {0} {1} - {2} send".format(coords, min_date, max_date)
            media = self.__api.media_search(lat=coords[0], lng=coords[1], distance=distance, \
                max_timestamp=max_stamp, count=self.MAX_SEARCH_COUNT)
            print "Answer for {0} {1} - {2} received".format(coords, min_date, max_date)

            if len(media) == 0:
                break

            self.__cals_tags(tags, media, max_stamp, min_date, ignore_list)

            if max_stamp <= datetime_to_timestamp(media[-1].created_time):
                max_stamp = max_stamp - 3600
            else:
                max_stamp = datetime_to_timestamp(media[-1].created_time)
        return tags


    def __cals_tags(self, tags, media, max_timestamp, min_timestamp, ignore_list):
        for m in media:
            dt = datetime_to_timestamp(m.created_time)
            if dt < max_timestamp and dt >= min_timestamp:
                try:
                    for t in m.tags:
                        if t.name not in ignore_list:
                            if not t.name in tags:
                                tags[t.name] = 1
                            else:
                                tags[t.name] += 1
                except AttributeError:
                    pass
            #else:
            #    print "missed {0}".format(datetime_to_timestamp(m.created_time))
