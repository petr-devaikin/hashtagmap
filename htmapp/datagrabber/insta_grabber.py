# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.helper import datetime_to_timestamp
import operator
from instagram.bind import InstagramAPIError, InstagramClientError

import threading

class InstaGrabberBanException(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message

class InstaGrabber:
    MAX_SEARCH_COUNT = 100

    def __init__(self, client_id, client_secret):
        self.__api = InstagramAPI(client_id=client_id, client_secret=client_secret)


    def find_tags(self, coords, distance, max_date, min_date, logger):
        self.all_media = []
        max_stamp = max_date
        attempts = 3
        while max_stamp > min_date:
            #print "Request for {0} {1} - {2} send".format(coords, min_date, max_date)
            try:
                logger.debug("Request send {0}".format(threading.current_thread().ident))
                media = self.__api.media_search(lat=coords[0], lng=coords[1], distance=distance, \
                    max_timestamp=max_stamp, count=self.MAX_SEARCH_COUNT)
            except InstagramAPIError as ex:
                if ex.error_type == "Rate limited":
                    raise InstaGrabberBanException(ex.error_message, ex.status_code)
                else:
                    raise ex
            except InstagramClientError as ex:
                if attempts > 0:
                    attempts = attempts - 1
                    continue
                else:
                    raise ex
            logger.debug("Answer received {0}".format(threading.current_thread().ident))
            #print "Answer for {0} {1} - {2} received".format(coords, min_date, max_date)

            if len(media) == 0:
                break

            for m in media:
                if not m in self.all_media:
                    self.all_media.append(m)

            if max_stamp <= datetime_to_timestamp(media[-1].created_time):
                max_stamp = max_stamp - 3600
            else:
                max_stamp = datetime_to_timestamp(media[-1].created_time)


    def calc_tags(self, max_timestamp, min_timestamp):
        tags = {}
        for m in filter(lambda am: datetime_to_timestamp(am.created_time) < max_timestamp and datetime_to_timestamp(am.created_time) >= min_timestamp ,
            self.all_media):
            try:
                for t in m.tags:
                    if not t.name in tags:
                        tags[t.name] = 1
                    else:
                        tags[t.name] += 1
            except AttributeError:
                pass
        return tags
            #else:
            #    print "missed {0}".format(datetime_to_timestamp(m.created_time))
