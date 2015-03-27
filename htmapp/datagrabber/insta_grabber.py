# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
from instagram.helper import datetime_to_timestamp
from instagram.bind import InstagramAPIError, InstagramClientError

import threading
import re

pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)


class InstaGrabberBanException(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "({0}) {1}".format(self.status_code, self.error_message)
        else:
            return self.error_message


class InstaGrabber:
    MAX_SEARCH_COUNT = 100
    MAX_ATTEMPTS = 3

    def __init__(self, client_id, client_secret):
        self.__api = InstagramAPI(client_id=client_id, client_secret=client_secret)

    def find_tags(self, coords, distance, max_date, min_date, logger):
        self.all_media = set()
        max_stamp = max_date
        attempts = self.MAX_ATTEMPTS

        while max_stamp > min_date:
            try:
                logger.debug("Send request {0}: lat:{1} long:{2} dist:{3} max:{4} count:{5}".format(
                    threading.current_thread().ident, coords[0], coords[1], distance, max_stamp, self.MAX_SEARCH_COUNT))
                media = self.__api.media_search(lat=coords[0], lng=coords[1], distance=distance,
                    max_timestamp=max_stamp, count=self.MAX_SEARCH_COUNT)
            except InstagramAPIError as ex:
                if ex.error_type == "Rate limited":
                    raise InstaGrabberBanException(ex.error_message, ex.status_code)
                else:
                    raise ex
            except InstagramClientError as ex:
                if attempts > 0:
                    attempts -= 1
                    continue
                else:
                    raise ex
            logger.debug("Answer received {0}".format(threading.current_thread().ident))

            if len(media) == 0: break

            self.all_media |= set(media)

            if max_stamp <= datetime_to_timestamp(media[-1].created_time):
                max_stamp = max_stamp - 3600
            else:
                max_stamp = datetime_to_timestamp(media[-1].created_time)


    def calc_tags(self, max_timestamp, min_timestamp):
        tags = {}

        def is_media_in_range(m):
            return datetime_to_timestamp(m.created_time) < max_timestamp and \
                   datetime_to_timestamp(m.created_time) >= min_timestamp

        for m in filter(is_media_in_range, self.all_media):
            try:
                for t in m.tags:
                    utf_tag = pattern.sub('', t.name)
                    if not utf_tag:
                        continue
                    if not utf_tag in tags:
                        tags[utf_tag] = 0
                    tags[utf_tag] += 1
            except AttributeError:
                pass
        return tags
