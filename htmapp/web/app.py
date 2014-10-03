# -*- coding: utf-8 -*-
from flask import current_app, Blueprint, render_template, abort, redirect, url_for
import pytz
from htmapp.db.db_engine import get_db

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
    from htmapp.db.models.location import Location
    from htmapp.db.models.simple_area import SimpleArea
    from htmapp.db.models.area_group import AreaGroup
    from htmapp.db.models.ignore_for_location import IgnoreForLocation
    from peewee import DoesNotExist

    if location_name == None:
        location = Location.get()
        return redirect(url_for('htm_app.index', location_name=location.name))
    try:
        location = Location.get(Location.name == location_name)
    except DoesNotExist:
        return abort(404)

    lat_km = (location.north - location.south) / location.height * 1000
    long_km = (location.east - location.west) / (location.north_width + location.south_width) * \
        2 * 1000

    areas = location.simple_areas
    max_count = location.simple_areas.order_by(SimpleArea.most_popular_tag_count.desc()).first().most_popular_tag_count
    if max_count == None:
        max_count = 0

    max_count = 0
    groups = location.area_groups
    for g in groups:
        if g.normal_count() > max_count:
            max_count = g.normal_count()

    ignore_list = current_app.config['COMMON_IGNORE'] + [t.tag for t in location.ignore_list]
    ignore_list = sorted(ignore_list)

    if location.updated:
        updated_time = location.updated.replace(tzinfo=pytz.timezone('GMT'))
        updated_time = updated_time.astimezone(pytz.timezone(location.timezone)).replace(tzinfo=None)
    else:
        updated_time = ''

    return render_template('index.html', max_count=max_count, lat_km=lat_km,
        long_km=long_km, location=location, location_list=Location.select(), groups=groups,
        ignore_list=ignore_list, updated_time=updated_time,
        map_key=current_app.config['GOOGLE_MAP_KEY'])
