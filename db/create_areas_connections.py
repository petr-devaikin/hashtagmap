# -*- coding: utf-8 -*-
from .models import *
from .. import config

db.init(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)

def create_areas_connections():
    for area in SimpleArea.select():
        area.add_connections()