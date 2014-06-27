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
    for a in areas:
        print a
        if a.most_popular_tag() != None and a.most_popular_tag().count_sum > max_count:
            max_count = a.most_popular_tag().count_cum
    print 'Done2'
    return render_template('index.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km)

if __name__ == '__main__':
    app.run(debug=True)