# -*- coding: utf-8 -*-
DEBUG = True
SECRET_KEY = 'development key'

DB_NAME = 'database'
DB_USER = 'user'
DB_PASSWORD = 'password'

COMMON_IGNORE = [u'instasize', u'love',
    u'vsco', u'vscocam', u'vscophoto', u'vscogood', u'vscobest', u'vscodaily', u'vscolike',
    u'vscoonly', u'vscophoto', u'vscom', u'vscocamera', u'vscoawar', u'vscostyle', u'vscovibe', u'vscophil',
    u'vscosummer', u'instavsco', u'vscogrid', u'vsco_food',
    u'follow', u'followme', u'followmeback', u'followhim', u'followher',
    u'instamood', u'instagood', u'instagram', u'instatags4likes', u'likeforlike', u'like4like', u'instacollage',
    u'tagsforlikes']

GOOGLE_MAP_KEY = ''

LOGINS = [{ 'CLIENT_ID': '', 'CLIENT_SECRET': '' }]

TAGS_TIME_PERIOD = 3600

LOG_FILE = '/tmp/userapi.log'
LOG_FORMAT = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'