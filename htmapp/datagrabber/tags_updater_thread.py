# -*- coding: utf-8 -*-
import threading
import Queue
from insta_grabber import *
from instagram.bind import InstagramAPIError

from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.hashtag_frequency import HashtagFrequency

import calendar
import datetime

class TagsUpdaterThread(threading.Thread):
    def __init__(self, areas_queue, db_lock, logins, logger):
        super(TagsUpdaterThread, self).__init__()
        self.queue = areas_queue
        self.db_lock = db_lock
        self.logins = logins
        self.grabber = self._get_grabber()
        self._stop = threading.Event()
        self.logger = logger
    
    _pass_everything = False
    _current_client = 0

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            try:
                area = self.queue.get(timeout=1)
                if not self._pass_everything:
                    self.logger.debug("Areas left: {0}".format(self.queue.qsize()))

                try:
                    if not self._pass_everything:
                        self.update_tags_for_area(area)
                except InstagramAPIError as ex:
                    self.logger.debug("Instagram API error. Area {0} is not processed: {1}".format(area.id, ex))
                except Exception as ex:
                    self.logger.error("Area {0} is not processed: {1}".format(area.id, ex))
                finally:
                    self.queue.task_done()

            except Queue.Empty:
                continue

    def _get_grabber(self):
        return InstaGrabber(self.logins[self._current_client]['CLIENT_ID'],
            self.logins[self._current_client]['CLIENT_SECRET'])

    def _change_client(self):
        self._current_client += 1
        if len(self.logins) <= self._current_client:
            return False
        else:
            self.grabber = self._get_grabber()
            return True

    def update_tags_for_area(self, area_hour):
        area = area_hour.area
        max_stamp = calendar.timegm(area_hour.max_stamp.timetuple())
        min_stamp = calendar.timegm(area_hour.min_stamp.timetuple())

        tags = self.grabber.find_tags((area.latitude, area.longitude), area.radius, \
            max_stamp, min_stamp)

        for tag_name in tags:
            self.db_lock.acquire()
            hashtag = Hashtag.get_or_create(name=tag_name)
            self.db_lock.release()
            HashtagFrequency.create(area_in_hour=area_hour, hashtag=hashtag, count=tags[tag_name])

        area_hour.processed = datetime.datetime.now()
        area_hour.save()

        self.logger.debug("+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area_hour.hashtag_counts.count()))
