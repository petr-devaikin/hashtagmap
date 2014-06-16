# -*- coding: utf-8 -*-
import time
from insta_grabber import InstaGrabber

common_ignore = [u"instasize", u"vscocam", u"vsco"]

client_id = "fd2526cfad7d4aaa948d20314b938132"
client_secret = "348777df18ea4fceb1df573528757bb0"
moscow_coords = (55.7522200, 37.6155600)
ostankino_coords = (55.735910, 37.606734)
distance = 1000

now = time.time()

grabber = InstaGrabber(client_id, client_secret)
common_ignore 
grabber.find_tags(ostankino_coords, distance, now, now - 24 * 3600, [u"moscow", u"москва", u"russia"] + common_ignore)

