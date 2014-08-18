# -*- coding: utf-8 -*-
from flask import current_app
from logging.handlers import TimedRotatingFileHandler
import logging

def get_logger():
    return current_app.logger

def set_logger_params(app):
    handler = TimedRotatingFileHandler(app.config['LOG_FILE'], when='D', interval=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(handler)