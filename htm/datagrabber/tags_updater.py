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
                self.queue.put(area)
                print "Area {0} returned to queue".format(area.id)
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
    max_stamp = last_memory_time

    for location in Location.select():
        if location.updated == None:
            location.updated = now - small_delta
            location.save()

        hours_to_clear = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << location.simple_areas, 
            (TagsOfAreaInHour.max_stamp < last_memory_time) | \
            (TagsOfAreaInHour.max_stamp > location.updated))

        print "Location {0}: {1} hours to clean".format(location.name, hours_to_clear.count())

        HashtagFrequency.delete().where(HashtagFrequency.area_in_hour << hours_to_clear).execute()
        TagsOfAreaInHour.delete().where(TagsOfAreaInHour.area << location.simple_areas, 
            (TagsOfAreaInHour.max_stamp < last_memory_time) | \
            (TagsOfAreaInHour.max_stamp > location.updated)).execute()

        for area in SimpleArea.select().where(SimpleArea.location == location):
            cur_max_time = location.updated
            while cur_max_time + small_delta <= now:
                tah = TagsOfAreaInHour.create(area=area, \
                    max_stamp=cur_max_time+small_delta, \
                    min_stamp=cur_max_time)
                areas_queue.put(tah)

                if cur_max_time > max_stamp:
                    cur_max_time = max_stamp

                cur_max_time = cur_max_time + small_delta

    # hope that putting is faster than processing
    areas_queue.join()

    for location in Location.select():
        location.updated = max_stamp
        location.save()

    for t in threads:
        t.stop()

    for t in threads:
        t.join()

    print 'Done'