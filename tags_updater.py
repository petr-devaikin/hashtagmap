# -*- coding: utf-8 -*-
import time
import datetime
from db.models import *
from datagrabber.insta_grabber import *
from .config import *
import threading
import Queue

class TagsUpdater(threading.Thread):
    def __init__(self, areas_queue, db_lock, max_stamp, min_stamp):
        super(TagsUpdater, self).__init__()
        self.queue = areas_queue
        self.db_lock = db_lock
        self.max_stamp = max_stamp
        self.min_stamp = min_stamp
        self.grabber = InstaGrabber(CLIENT_ID, CLIENT_SECRET)

    def run(self):
        try:
            while self.queue.qsize() > 0:
                print "Areas left: {0}".format(self.queue.qsize())
                try:
                    area = self.queue.get(False)
                    self.update_tags_for_area(area)
                    self.queue.task_done()
                except Empty:
                    pass
        finally:
            pass

    def update_tags_for_area(self, area):
        HashtagFrequency.delete().where(HashtagFrequency.simple_area == area).execute()

        tags = self.grabber.find_tags((area.latitude, area.longitude), area.radius, \
            self.max_stamp, self.min_stamp, COMMON_IGNORE)

        for tag_name in tags:
            self.db_lock.acquire()
            hashtag = Hashtag.get_or_create(name=tag_name)
            self.db_lock.release()
            HashtagFrequency.create(simple_area=area, hashtag=hashtag, count=tags[tag_name])

        area.updated = datetime.datetime.now()
        area.save()

        print "+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area.hashtag_counts.count())


def update_tags(time_delta=120, threads_count=50):
    db.init(DB_NAME, user=DB_USER, password=DB_PASSWORD)

    areas_queue = Queue.Queue()
    lock = threading.Lock()
    now = time.time()
    for area in SimpleArea.select():
        areas_queue.put(area)

    threads = []
    for i in range(threads_count):
        t = TagsUpdater(areas_queue, lock, now, now - time_delta)
        threads.append(t)
        t.start()

    for i in range(threads_count):
        threads[i].join()