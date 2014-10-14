# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Hashtag Map',
    version='1.1',
    packages=['htmapp'],
    author='Petr Devaikin',
    author_email='p.devaikin@gmail.com',
    url='http://hashtag-urbanmap.rhcloud.com/',
    include_package_data=True,
    zip_safe=False,
    setup_requires=['Flask'],
    install_requires=['Flask', 'peewee', 'Flask-Script', 'MySQL-Python', 'python-instagram', 'pytz']
)
