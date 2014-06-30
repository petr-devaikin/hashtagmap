# -*- coding: utf-8 -*-
from flask import Flask, render_template
from htm.db.models import *
from htm import config

# configure
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(app)

# init db
db.init(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)

@app.route('/')
def hello_world():
    location = Location.get()

    lat_km = (location.north - location.south) / location.height * 1000
    long_km = (location.east - location.west) / (location.north_width + location.south_width) * \
        2 * 1000

    areas = location.simple_areas
    max_count = 0
    print 'Done1'

    ignore = [] + config.COMMON_IGNORE
    for tag in location.ignore_list:
        ignore.append(tag.tag)

    for a in areas:
        if a.most_popular_tag(ignore) != None and \
                a.most_popular_tag().count > max_count:
            max_count = a.most_popular_tag().count
    print 'Done2'
    return render_template('index.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km)


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
        long_km=long_km)

if __name__ == '__main__':
    app.run(debug=True)