# -*- coding: utf-8 -*-
DEBUG = True
SECRET_KEY = 'development key'

DATABASE = {
    'ENGINE': 'MySQL',
    'NAME': 'database',
    'PARAMS': { 'user': 'user', 'password': 'password', 'host': 'localhost', 'port': 8888 }
}

COMMON_IGNORE = [u'instasize', u'love',
    u'vsco', u'vscocam', u'vscophoto', u'vscogood', u'vscobest', u'vscodaily', u'vscolike',
    u'vscoonly', u'vscophoto', u'vscom', u'vscocamera', u'vscoawar', u'vscostyle', u'vscovibe', u'vscophil',
    u'vscosummer', u'instavsco', u'vscogrid', u'vsco_food', u'vscolove', u'vscolover', u'vscovsco',
    u'vscogang', u'vscofeature', u'vscophile', u'vscoinspiration',
    u'follow', u'followme', u'followmeback', u'followhim', u'followher', u'photooftheday',
    u'instamood', u'instagood', u'instagram', u'instatags4likes', u'likeforlike', u'like4like', u'instacollage',
    u'tagsforlikes']

GOOGLE_MAP_KEY = ''

LOGINS = ({ 'CLIENT_ID': '', 'CLIENT_SECRET': '' }, )

REQUEST_THREADS_COUNT = 10
SUMMARIZE_THREADS_COUNT = 30
TAGS_MEMORY = 24 * 3600
TAGS_TIME_PERIOD = 3600

COLOR_GROUP_COUNT = 7

OLD_TAG_REMOVE_LIMIT = 1000

LOGGER = {
    'FORMAT': '[%(asctime)s] %(filename)s[%(lineno)d] #%(levelname)-8s  %(message)s',
    'PATH': '/var/log/hashtagmap/htm.log',
    'DEBUG_PATH': '/var/log/hashtagmap/htm-debug.log'
}