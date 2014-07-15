# -*- coding: utf-8 -*-
from htmapp.db.models import *


class TagGroup(object):
    def __init__(self, area):
        self.left = self.right = area.column
        self.top = self.bottom = area.row
        self.tag_name = area.most_popular_tag_name
        self.count = area.most_popular_tag_count

    def expand(self, new_elements):
        for a in new_elements:
            if a.column > self.right:
                self.right = a.column
            if a.column < self.left:
                self.left = a.column
            if a.row > self.bottom:
                self.bottom = a.row
            if a.row < self.top:
                self.top = a.row
            self.count += a.most_popular_tag_count


class TagsGrpouper(object):
    def __init__(self, location_id):
        self.location = Location.get(id=location_id)

    def process(self):
        queue = []
        groups = []
        for a in self.location.simple_areas:
            if a.most_popular_tag_count != None:
                queue.append(a)

        while len(queue) > 0:
            area = queue.pop()
            group = TagGroup(area)
            can_expand = True
            while can_expand:
                to_the_right = filter(lambda x: x.column == group.right + 1 and \
                    x.row <= group.top and x.row >= group.bottom,
                    queue)
                can_expand = len(to_the_right) == group.bottom - group.top + 1
                if can_expand:
                    for a in to_the_right:
                        if a.most_popular_tag_name != group.tag_name:
                            can_expand = False
                            break
                if can_expand:
                    group.expand(to_the_right)
                    for a in to_the_right:
                        queue.remove(a)
            groups.append(group)
        return groups

