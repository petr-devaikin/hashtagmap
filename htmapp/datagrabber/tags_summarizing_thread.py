# -*- coding: utf-8 -*-
import threading
import Queue
from htmapp.db.models import *

class TagsSummarizingThread(threading.Thread):
    def __init__(self, areas_queue, common_ignore):
        super(TagsSummarizingThread, self).__init__()
        self.queue = areas_queue
        self.common_ignore = common_ignore

    def run(self):
        while True:
            try:
                area = self.queue.get(False)
                print "Areas left: {0}".format(self.queue.qsize())
                self.recalc_tags_for_area(area)
                self.queue.task_done()
            except Queue.Empty:
                break


    def recalc_tags_for_area(self, area):
        for hour in area.tags_in_hour:
            for tag_count in hour.hashtag_counts:
                sum_count = HashtagFrequencySum.get_or_create(hashtag=tag_count.hashtag, area=area)
                sum_count.count += tag_count.count
                sum_count.save()

        ignore = [] + self.common_ignore
        for tag in area.location.ignore_list:
            ignore.append(tag.tag)
        area.calc_most_popular_tag(ignore)

        print "Area {0} of {1} recalculated".format(area.id, area.location.name)
