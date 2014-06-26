# -*- coding: utf-8 -*-
import calendar
import time
import datetime
from ..db.models import *
from .insta_grabber import *
from ..config import *
import threading
import Queue

class TagsUpdater(threading.Thread):
    def __init__(self, areas_queue, db_lock):
        super(TagsUpdater, self).__init__()
        self.queue = areas_queue
        self.db_lock = db_lock
        self.grabber = InstaGrabber(CLIENT_ID, CLIENT_SECRET)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while not self.stopped():
            try:
                area = self.queue.get(timeout=1)
                print "Areas left: {0}".format(self.queue.qsize())
            except Queue.Empty:
                continue

            try:
                self.update_tags_for_area(area)
            except:
                print "Area {0} is not processed".format(area.id)
            finally:
                self.queue.task_done()

    def update_tags_for_area(self, area_hour):
        area = area_hour.area
        max_stamp = calendar.timegm(area_hour.max_stamp.timetuple())
        min_stamp = calendar.timegm(area_hour.min_stamp.timetuple())

        tags = self.grabber.find_tags((area.latitude, area.longitude), area.radius, \
            max_stamp, min_stamp, COMMON_IGNORE)

        for tag_name in tags:
            self.db_lock.acquire()
            hashtag = Hashtag.get_or_create(name=tag_name)
            self.db_lock.release()
            HashtagFrequency.create(area_in_hour=area_hour, hashtag=hashtag, count=tags[tag_name])

        area_hour.processed = datetime.datetime.now()
        area_hour.save()

        print "+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area_hour.hashtag_counts.count())


def update_tags(threads_count=100, memory=24 * 3600):
    db.init(DB_NAME, user=DB_USER, password=DB_PASSWORD)

    areas_queue = Queue.Queue()
    lock = threading.Lock()

    threads = []
    for i in range(threads_count):
        t = TagsUpdater(areas_queue, lock)
        threads.append(t)
        t.start()

    now = datetime.datetime.now()
    last_memory_time = now + datetime.timedelta(seconds=-memory)
    small_delta = datetime.timedelta(seconds=TIME_DELTA)

    for location in Location.select():
        if location.updated == None:
            start_time = now - small_delta
        else:
            start_time = location.updated

        location.clear_old_hours(last_memory_time)

        # process not processed areas
        for tah in TagsOfAreaInHour.select().where(TagsOfAreaInHour.processed == None, \
                    TagsOfAreaInHour.area << location.simple_areas):
            areas_queue.put(tah)

        # add new areas
        for area in SimpleArea.select().where(SimpleArea.location == location):
            cur_max_time = start_time
            while cur_max_time + small_delta <= now:
                tah = TagsOfAreaInHour.create(area=area, \
                    max_stamp=cur_max_time+small_delta, \
                    min_stamp=cur_max_time)
                areas_queue.put(tah)

                cur_max_time = cur_max_time + small_delta

        location.update_time()


    # hope that putting is faster than processing
    areas_queue.join()

    for t in threads:
        t.stop()

    for t in threads:
        t.join()

    print 'Done'