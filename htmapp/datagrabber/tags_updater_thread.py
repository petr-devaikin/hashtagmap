# -*- coding: utf-8 -*-
import threading
import Queue
from insta_grabber import *

from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.hashtag_frequency import HashtagFrequency
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour

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
        try:
            while not self.stopped():
                try:
                    area = self.queue.get(timeout=1)
                    if not self._pass_everything:
                        self.logger.debug("Areas left: {0}".format(self.queue.qsize()))

                        try:
                            self.update_tags_for_area(area)
                        except InstaGrabberBanException as ex:
                            self.logger.debug("Instagram banned me. Area {0} is not processed: {1}".format(area.id, ex))
                            if not self._change_client():
                                self.logger.debug("Last instagram client expired")
                                self._pass_everything = True
                        except Exception as ex:
                            self.logger.exception("Area {0} is not processed: {1}".format(area.id, ex))
                    
                    self.queue.task_done()

                except Queue.Empty:
                    continue
        except Exception as ex:
            self.logger.exception('Thread crashed!')


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

    def update_tags_for_area(self, area):
        area_hours = TagsOfAreaInHour.select().where(TagsOfAreaInHour.processed == None,
                    TagsOfAreaInHour.area == area)

        area_max_stamp = calendar.timegm(area_hours.order_by(TagsOfAreaInHour.max_stamp.desc())[0].max_stamp.timetuple())
        area_min_stamp = calendar.timegm(area_hours.order_by(TagsOfAreaInHour.max_stamp)[0].min_stamp.timetuple())

        #print "Area min max", area_min_stamp, area_max_stamp

        self.grabber.find_tags((area.latitude, area.longitude), area.radius,
            area_max_stamp, area_min_stamp, self.logger)

        for area_hour in area_hours:
            # if something happened while updating and processed flag was not set up
            for htf in area_hour.hashtag_counts:
                htf.delete_instance()

            #print "Updating {0}".format(area_hour.id)
            max_stamp = calendar.timegm(area_hour.max_stamp.timetuple())
            min_stamp = calendar.timegm(area_hour.min_stamp.timetuple())
            tags = self.grabber.calc_tags(max_stamp, min_stamp)

            #print "{0} tags found".format(len(tags))

            i = 0
            for tag_name in tags:
                self.db_lock.acquire()
                hashtag = Hashtag.get_or_create(name=tag_name)
                self.db_lock.release()
                i += 1
                try:
                    HashtagFrequency.create(area_in_hour=area_hour, hashtag=hashtag, count=tags[tag_name])
                except Exception:
                    self.logger.exception("Duplicate {2}: {0} > {1}, {3}".format(len(tags), len(set(tags)), i, hashtag.name == tag_name))

            area_hour.processed = datetime.datetime.now()
            area_hour.save()

        self.logger.debug("+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area_hour.hashtag_counts.count()))
