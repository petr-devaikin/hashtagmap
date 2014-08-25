# -*- coding: utf-8 -*-
from flask import Flask
from htmapp.web.app import htm_app
from htmapp.logger import set_logger_params
from htmapp.db.db_engine import init_db
import os

# configure
def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('htmapp.default_settings')
    app.config.from_pyfile('application.cfg', silent=True)
    app.config.from_pyfile(os.environ['HASHTAGMAP_SETTINGS'], silent=True)

    if config_object != None:
        app.config.from_object(config_object)

    return app

def init_app(app):
    set_logger_params(app)
    init_db(app)

    app.register_blueprint(htm_app)
