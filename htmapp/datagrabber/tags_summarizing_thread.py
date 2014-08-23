# -*- coding: utf-8 -*-
import threading
import Queue
from htmapp.db.models.hashtag_frequency_sum import HashtagFrequencySum
from htmapp.db.models.hashtag_frequency import HashtagFrequency
from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.simple_area import SimpleArea
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour
from htmapp.db.models.ignore_for_location import IgnoreForLocation
from peewee import fn

class TagsSummarizingThread(threading.Thread):
    def __init__(self, areas_queue, common_ignore, logger):
        super(TagsSummarizingThread, self).__init__()
        self.queue = areas_queue
        self.common_ignore = common_ignore
        self.logger = logger

    def run(self):
        while True:
            try:
                area = self.queue.get(False)
                self.logger.debug("Areas left: {0}".format(self.queue.qsize()))
                self.recalc_tags_for_area(area)
                self.queue.task_done()
            except Queue.Empty:
                break

    @staticmethod
    def calc_most_popular_tag_for_area(area, ignore=[]):
        sq = area.hashtag_counts_sum.join(Hashtag)
        where = sq.where(~(Hashtag.name << ignore)).order_by(HashtagFrequencySum.count.desc())
        tag = where.first()
        if tag == None:
            area.most_popular_tag_name = None
            area.most_popular_tag_count = None
        else:
            area.most_popular_tag_name = tag.hashtag.name
            area.most_popular_tag_count = tag.count
        area.save()


    def recalc_tags_for_area(self, area):
        select = HashtagFrequency.select(HashtagFrequency.area_in_hour, HashtagFrequency.hashtag, fn.Sum(HashtagFrequency.count).alias('sum'))
        join = select.join(TagsOfAreaInHour).join(SimpleArea)
        where = join.where(TagsOfAreaInHour.area == area)
        group = where.group_by(HashtagFrequency.hashtag, TagsOfAreaInHour.area)

        for h in group:
            sum_count = HashtagFrequencySum(hashtag=h.hashtag, area=h.area_in_hour.area)
            sum_count.count = h.sum
            sum_count.save()

        ignore = [] + self.common_ignore
        for tag in area.location.ignore_list:
            ignore.append(tag.tag)
        TagsSummarizingThread.calc_most_popular_tag_for_area(area, ignore)

        self.logger.debug("Area {0} of {1} recalculated".format(area.id, area.location.name))
