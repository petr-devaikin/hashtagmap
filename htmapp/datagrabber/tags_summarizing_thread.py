# -*- coding: utf-8 -*-
import threading
import Queue
from htmapp.db.models.hashtag_frequency import HashtagFrequency
from htmapp.db.models.hashtag import Hashtag
from htmapp.db.models.tags_of_area_in_hour import TagsOfAreaInHour
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

    def recalc_tags_for_area(self, area):
        ignore = list(self.common_ignore) + [tag for tag in area.location.ignore_list]

        hf_sum = fn.Sum(HashtagFrequency.count)

        select = Hashtag.select(Hashtag, hf_sum.alias('sum')).join(HashtagFrequency).join(TagsOfAreaInHour)
        where = select.where(TagsOfAreaInHour.area == area, ~(Hashtag.name << ignore))
        group = where.group_by(Hashtag).order_by(hf_sum.desc())

        if group.count() > 0:
            tag = group.get()
            area.most_popular_tag_name = tag.name
            area.most_popular_tag_count = tag.sum
        else:
            area.most_popular_tag_name = None
            area.most_popular_tag_count = None
        area.save()

        self.logger.debug("Area {0} of {1} recalculated".format(area.id, area.location.name))
