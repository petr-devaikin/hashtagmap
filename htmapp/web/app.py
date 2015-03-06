# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, render_template, abort, redirect, url_for
import json
from htmapp.db.db_engine import get_db
from htmapp.db.models.location import Location
from htmapp.db.models.simple_area import SimpleArea
from htmapp.db.models.area_group import AreaGroup
from htmapp.db.models.ignore_for_location import IgnoreForLocation
from peewee import DoesNotExist

htm_app = Blueprint('htm_app', __name__)

@htm_app.before_request
def before_request():
    db = get_db()
    db.connect()

@htm_app.after_request
def after_request(response):
    db = get_db()
    db.close()
    return response

@htm_app.route('/')
@htm_app.route('/<location_name>')
def index(location_name=None):
    if location_name == None:
        location = Location.get()
        return redirect(url_for('htm_app.index', location_name=location.name))
    try:
        location = Location.get(Location.name == location_name)
    except DoesNotExist:
        return abort(404)

    groups = [g.to_dict() for g in location.area_groups]

    ignore_list = current_app.config['COMMON_IGNORE'] + [t.tag for t in location.ignore_list]
    ignore_list.sort()

    max_count = max([g['count'] for g in groups]) if groups else 0

    legend = []
    group_count = current_app.config['COLOR_GROUP_COUNT']


    for i in range(group_count):
        k1 = pow((float(i) / group_count), 2)
        k2 = pow((float(i + 1) / group_count), 2)
        legend.append({
            'min': int((max_count - 1) * k1) + 1,
            'max': int((max_count - 1) * k2) + 1,
        })

    return render_template('index.html', max_count=max_count, groups=json.dumps(groups),
        location=location, location_list=Location.select().order_by(Location.name.desc()), 
        ignore_list=ignore_list, map_key=current_app.config['GOOGLE_MAP_KEY'],
        legend=legend, legend_json=json.dumps(legend))
