# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='Hashtag Map',
    version='1.0',
    long_description=__doc__,
    packages=['htmapp'],
    author='Petr Devaikin',
    author_email='p.devaikin@gmail.com',
    include_package_data=True,
    zip_safe=False,
    setup_requires=['Flask'],
    install_requires=['Flask', 'peewee', 'Flask-Script', 'MySQL-Python', 'python-instagram', 'pytz']
)
