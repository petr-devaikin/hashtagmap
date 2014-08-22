# -*- coding: utf-8 -*-
DEBUG = True
SECRET_KEY = 'development key'

DB_NAME = 'database'
DB_USER = 'user'
DB_PASSWORD = 'password'

COMMON_IGNORE = [u'instasize', u'love',
    u'vsco', u'vscocam', u'vscophoto', u'vscogood', u'vscobest', u'vscodaily', u'vscolike',
    u'vscoonly', u'vscophoto', u'vscom', u'vscocamera', u'vscoawar', u'vscostyle', u'vscovibe', u'vscophil',
    u'vscosummer', u'instavsco', u'vscogrid', u'vsco_food', u'vscolove', u'vscolover', u'vscovsco',
    u'follow', u'followme', u'followmeback', u'followhim', u'followher',
    u'instamood', u'instagood', u'instagram', u'instatags4likes', u'likeforlike', u'like4like', u'instacollage',
    u'tagsforlikes']

GOOGLE_MAP_KEY = ''

LOGINS = [{ 'CLIENT_ID': '', 'CLIENT_SECRET': '' }]

UPDATE_THREADS_COUNT = 50
TAGS_MEMORY = 24 * 3600
TAGS_TIME_PERIOD = 3600

LOG_FILE = '/tmp/hashtagmap.log'
LOG_FILE_DEBUG = '/tmp/hashtagmap-debug.log'
LOG_FORMAT = '[%(asctime)s] %(filename)s[%(lineno)d] #%(levelname)-8s  %(message)s'