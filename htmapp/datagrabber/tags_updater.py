# -*- coding: utf-8 -*-
import time
import datetime
import pytz

from htmapp.db.models.hashtag_frequency import HashtagFrequency
from htmapp.db.models.hashtag_frequency_sum import HashtagFrequencySum
from htmapp.db.models.location import Location
from htmapp.db.models.simple_area import SimpleArea
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour

from tags_updater_thread import TagsUpdaterThread
from tags_summarizing_thread import TagsSummarizingThread
from flask import current_app
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
        t = TagsSummarizingThread(areas_queue, current_app.config['COMMON_IGNORE'])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def clear_old_hours(location, min_time):
    hours_to_clear = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << location.simple_areas, 
        TagsOfAreaInHour.max_stamp < min_time)
    count = hours_to_clear.count()

    HashtagFrequency.delete().where(HashtagFrequency.area_in_hour << hours_to_clear).execute()
    TagsOfAreaInHour.delete().where(TagsOfAreaInHour.area << location.simple_areas, 
        TagsOfAreaInHour.max_stamp < min_time).execute()

    print "Location {0}: {1} old hours to remove".format(location.name, count)

def update_location_time(location):
    all_hours = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << location.simple_areas).order_by(TagsOfAreaInHour.max_stamp.desc())
    if all_hours.count() == 0:
        location.updated = None
    else:
        location.updated = all_hours.first().max_stamp
    location.save()


def update_tags(threads_count=100, memory=24 * 3600):
    areas_queue = Queue.Queue()
    lock = threading.Lock()

    threads = []
    for i in range(threads_count):
        t = TagsUpdaterThread(areas_queue, lock, current_app.config['LOGINS'])
        threads.append(t)
        t.start()


    for location in Location.select():
        now = datetime.datetime.now(tz=pytz.timezone(location.timezone)).replace(tzinfo=None)
        last_memory_time = now - datetime.timedelta(seconds=memory)
        small_delta = datetime.timedelta(seconds=current_app.config['TAGS_TIME_PERIOD'])

        clear_old_hours(location, last_memory_time)
        update_location_time(location)

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
                tah = TagsOfAreaInHour.create(area=area,
                    max_stamp=cur_max_time+small_delta,
                    min_stamp=cur_max_time)
                areas_queue.put(tah)

            cur_max_time = cur_max_time + small_delta

        update_location_time(location)

    # hope that putting is faster than processing
    areas_queue.join()

    print 'Queue joint'

    for t in threads:
        t.stop()

    print 'Threads stopping'

    for t in threads:
        t.join()

    summarize_tags(threads_count)

    print 'Tags summarized'

    from htmapp.tags_processing.tags_grouper import TagsGrouper
    grouper = TagsGrouper(location.id)
    grouper.process()

    print 'Done'