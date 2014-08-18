# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response
from htmapp.logger import get_logger, set_logger_params

# configure
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('htmapp.default_settings')
app.config.from_pyfile('application.cfg', silent=True)

set_logger_params(app)

# init db
from htmapp.db.models.db_engine import get_db
db = get_db()
db.init(app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'])


@app.route('/')
def hello_world():
    from htmapp.db.models.location import Location
    from htmapp.db.models.simple_area import SimpleArea
    from htmapp.db.models.area_group import AreaGroup

    location = Location.get()

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

    return render_template('index.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km, location=location, groups=groups, map_key=app.config['GOOGLE_MAP_KEY'])

"""
@app.route('/<tag_name>')
def counts(tag_name):
    location = Location.get()

    lat_km = (location.north - location.south) / location.height * 1000
    long_km = (location.east - location.west) / (location.north_width + location.south_width) * \
        2 * 1000

    areas = location.simple_areas
    max_count = 0
    print 'Done1'
    for a in areas:
        count = a.count_of_tag(tag_name)
        a.c = count
        if count > max_count:
            max_count = count
    print 'Done2'
    return render_template('counts.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km, location=location)
"""