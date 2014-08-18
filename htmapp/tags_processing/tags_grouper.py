# -*- coding: utf-8 -*-
from htmapp.db.models.location import Location
from htmapp.db.models.simple_area import SimpleArea


class TagGroup(object):
    def __init__(self, area):
        self.id = area.id

        self.left = self.right = area.column
        self.top = self.bottom = area.row
        self.tag_name = area.most_popular_tag_name
        self.count = area.most_popular_tag_count

        self.north = self.south = area.latitude
        self.west = self.east = area.longitude

        self.radius = area.radius

    def expand(self, new_elements):
        for a in new_elements:
            if a.column > self.right:
                self.right = a.column
                self.east = a.longitude
            elif a.column < self.left:
                self.left = a.column
                self.west = a.longitude
            elif a.row > self.bottom:
                self.bottom = a.row
                self.south = a.latitude
            elif a.row < self.top:
                self.top = a.row
                self.north = a.latitude
            self.count += a.most_popular_tag_count

    def can_expand(self, new_areas):
        result = True
        for a in new_areas:
            if a.most_popular_tag_name != self.tag_name:
                result = False
                break
        return result

    def normal_count(self):
        return int(float(self.count) / (self.right - self.left + 1) / (self.bottom - self.top + 1))


class TagsGrpouper(object):
    def __init__(self, location_id):
        self.location = Location.get(id=location_id)

    def process(self):
        queue = []
        groups = []
        for a in self.location.simple_areas.order_by(SimpleArea.row, SimpleArea.column):
            if a.most_popular_tag_count != None:
                queue.append(a)

        while len(queue) > 0:
            area = queue.pop(0)
            group = TagGroup(area)
            can_expand = True
            while can_expand:
                can_expand = False

                to_the_right = filter(lambda x: x.column == group.right + 1 and \
                    x.row <= group.top and x.row >= group.bottom,
                    queue)
                if len(to_the_right) == group.bottom - group.top + 1 and group.can_expand(to_the_right):
                    can_expand = True
                    group.expand(to_the_right)
                    for a in to_the_right:
                        queue.remove(a)

                to_the_bottom = filter(lambda x: x.row == group.bottom + 1 and \
                    x.column <= group.right and x.column >= group.left,
                    queue)
                if len(to_the_bottom) == group.right - group.left + 1 and group.can_expand(to_the_bottom):
                    can_expand = True
                    group.expand(to_the_bottom)
                    for a in to_the_bottom:
                        queue.remove(a)
            groups.append(group)
        return groups

