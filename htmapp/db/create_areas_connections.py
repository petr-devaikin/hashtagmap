# -*- coding: utf-8 -*-
from htmapp.db.models import *

def create_areas_connections():
    for area in SimpleArea.select():
        area.add_connections()