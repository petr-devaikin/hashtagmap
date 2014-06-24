# -*- coding: utf-8 -*-
import time
import datetime
from db.models import *
from datagrabber.insta_grabber import *
from .config import *


def update_tags(time_delta):
    db.init(DB_NAME, user=DB_USER, password=DB_PASSWORD)

    grabber = InstaGrabber(CLIENT_ID, CLIENT_SECRET)
    now = time.time()

    for area in SimpleArea.select():
        HashtagFrequency.delete().where(HashtagFrequency.simple_area == area).execute()

        tags = grabber.find_tags((area.latitude, area.longitude), area.radius, now, now - time_delta, \
            COMMON_IGNORE)

        for tag_name in tags:
            hashtag = Hashtag.get_or_create(name=tag_name)
            HashtagFrequency.create(simple_area=area, hashtag=hashtag, count=tags[tag_name])

        area.updated = datetime.datetime.now
        area.save()

        print "+++ {2} tags for area {0} of {1} updated".format(area.id, area.location.name, area.hashtag_counts.count())
        print "Tags count: ", Hashtag.select().count()