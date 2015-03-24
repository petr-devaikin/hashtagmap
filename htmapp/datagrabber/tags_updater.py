# -*- coding: utf-8 -*-
import time
import datetime
import pytz
import threading
import Queue
from flask import current_app
from htmapp.db.models.hashtag_frequency import HashtagFrequency
from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.location import Location
from htmapp.db.models.simple_area import SimpleArea
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour
from htmapp.logger import get_logger
from htmapp.datagrabber.tags_summarizing_thread import TagsSummarizingThread
from htmapp.datagrabber.tags_updater_thread import TagsUpdaterThread
from htmapp.tags_processing.tags_grouper import TagsGrouper
from peewee import fn, JOIN_LEFT_OUTER

def clear_old_tags():
    get_logger().info("Start to remove old tags")
    select = Hashtag.select().join(HashtagFrequency, JOIN_LEFT_OUTER)
    select = select.group_by(Hashtag).having(fn.Count(HashtagFrequency.id) == 0).limit(1000)
    count = select.count()
    get_logger().info("{0} old tags to remove".format(count))


    for h in select:
        h.delete_instance()

    get_logger().info("Old tags to remove")


def summarize_tags(threads_count=100):
    get_logger().info('Summarizing starts')

    areas_queue = Queue.Queue()

    for area in SimpleArea.select(): areas_queue.put(area)

    threads = []
    for i in range(threads_count):
        t = TagsSummarizingThread(areas_queue, current_app.config['COMMON_IGNORE'], get_logger())
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

    get_logger().info("Location {0}: {1} old hours to remove".format(location.name, count))


def update_location_time(location):
    all_hours = TagsOfAreaInHour.select().where(TagsOfAreaInHour.area << location.simple_areas).order_by(TagsOfAreaInHour.max_stamp.desc())
    location.updated = all_hours.first().max_stamp if all_hours.count() else None
    location.save()


def update_tags(request_threads_count, summarize_threads_count, memory):
    get_logger().info('Tags update starts')

    clear_old_tags()
    return

    areas_queue = Queue.Queue()
    lock = threading.Lock()
    
    threads = []
    for i in range(request_threads_count):
        t = TagsUpdaterThread(areas_queue, lock, current_app.config['LOGINS'], get_logger())
        threads.append(t)
        t.start()

    for location in Location.select():
        now = datetime.datetime.now(tz=pytz.timezone('GMT')).replace(tzinfo=None)
        last_memory_time = now - datetime.timedelta(seconds=memory)
        small_delta = datetime.timedelta(seconds=current_app.config['TAGS_TIME_PERIOD'])

        clear_old_hours(location, last_memory_time)
        update_location_time(location)

        start_time = location.updated or last_memory_time

        get_logger().info("Add new hour-areas to {0}".format(location.name))

        # add new areas
        count = 0
        cur_max_time = start_time
        while cur_max_time + small_delta <= now:
            for area in SimpleArea.select().where(SimpleArea.location == location):
                tah = TagsOfAreaInHour.create(area=area,
                    max_stamp=cur_max_time + small_delta,
                    min_stamp=cur_max_time)
                count += 1

            cur_max_time += small_delta

        get_logger().info("{0} hour-areas added to {1}".format(count, location.name))

        update_location_time(location)

        # process not processed areas
        for area in location.simple_areas:
            if TagsOfAreaInHour.select().where(TagsOfAreaInHour.processed == None,
                    TagsOfAreaInHour.area == area).count() > 0:
                areas_queue.put(area)

    get_logger().info('Waiting for all threads')

    # hope that putting is faster than processing
    areas_queue.join()

    get_logger().info('Areas updated')

    for t in threads: t.stop()
    get_logger().debug('Threads stopping')

    for t in threads: t.join()
    
    clear_old_tags()

    summarize_tags(summarize_threads_count)

    get_logger().info('Tags summarized')

    for location in Location.select():
        grouper = TagsGrouper(location.id)
        grouper.process()
        get_logger().info("Tags groupped for {0}".format(location.name))

    get_logger().info('Tags update is done')