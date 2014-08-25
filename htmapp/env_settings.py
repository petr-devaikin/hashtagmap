# -*- coding: utf-8 -*-
import os

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']

GOOGLE_MAP_KEY = os.environ['GOOGLE_MAP_KEY']

LOGINS = [{ 'CLIENT_ID': os.environ['INSTA_ID1'], 'CLIENT_SECRET': os.environ['INSTA_KEY1'] },
    { 'CLIENT_ID': os.environ['INSTA_ID2'], 'CLIENT_SECRET': os.environ['INSTA_KEY2'] },
    { 'CLIENT_ID': os.environ['INSTA_ID3'], 'CLIENT_SECRET': os.environ['INSTA_KEY3'] }]


LOG_FILE = os.environ['LOG_FILE']
LOG_FILE_DEBUG = os.environ['LOG_DEBUG_FILE']