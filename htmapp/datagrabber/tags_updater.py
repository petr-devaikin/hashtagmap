# -*- coding: utf-8 -*-
import time
import datetime
from htmapp.db.models import *
from tags_updater_thread import TagsUpdaterThread
from tags_summarizing_thread import TagsSummarizingThread
import threading
import Queue


def summarize_tags(threads_count=100):
    print 'Summarizing start'

    areas_queue = Queue.Queue()

    for location in Location.select():
        HashtagFrequencySum.delete().where(HashtagFrequencySum.area << location.simple_areas).execute()

        for area in location.simple_areas:
            areas_queue.put(area)

    threads = []
    for i in range(threads_count):
        t = TagsSummarizingThread(areas_queue)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def update_tags(threads_count=100, memory=24 * 3600):
    areas_queue = Queue.Queue()
    lock = threading.Lock()

    threads = []
    for i in range(threads_count):
        t = TagsUpdaterThread(areas_queue, lock)
        threads.append(t)
        t.start()

    now = datetime.datetime.now()
    last_memory_time = now - datetime.timedelta(seconds=memory)
    small_delta = datetime.timedelta(seconds=TIME_DELTA)

    for location in Location.select():
        location.clear_old_hours(last_memory_time)
        location.update_time()

        if location.updated == None:
            start_time = last_memory_time
        else:
            start_time = location.updated

        # process not processed areas
        for tah in TagsOfAreaInHour.select().where(TagsOfAreaInHour.processed == None, \
                    TagsOfAreaInHour.area << location.simple_areas):
            areas_queue.put(tah)

        # add new areas
        cur_max_time = start_time
        while cur_max_time + small_delta <= now:
            for area in SimpleArea.select().where(SimpleArea.location == location):
                tah = TagsOfAreaInHour.create(area=area, \
                    max_stamp=cur_max_time+small_delta, \
                    min_stamp=cur_max_time)
                areas_queue.put(tah)

            cur_max_time = cur_max_time + small_delta

        location.update_time()

    # hope that putting is faster than processing
    areas_queue.join()

    print 'Queue joint'

    for t in threads:
        t.stop()

    print 'Threads stopping'

    for t in threads:
        t.join()

    summarize_tags(threads_count)

    print 'Done'
