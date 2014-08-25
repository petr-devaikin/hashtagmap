# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Hashtag Map',
    version='1.0',
    long_description=__doc__,
    packages=['htmapp'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'peewee', 'Flask-Script', 'MySQL-Python', 'python-instagram', 'pytz', 'psycopg2']
)
