# -*- coding: utf-8 -*-
from flask import Flask, render_template

import sys
sys.path.append("../")
sys.path.append("../db")

from models import *
import config

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
    areas = location.simple_areas
    max_count = HashtagFrequency.select().join(SimpleArea).where(SimpleArea.location == location)\
        .order_by(HashtagFrequency.count.desc()).get().count
    return render_template('index.html', areas=areas, max_count=max_count)

if __name__ == '__main__':
    app.run(debug=True)