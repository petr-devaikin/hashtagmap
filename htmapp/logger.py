# -*- coding: utf-8 -*-
from flask import current_app
from logging.handlers import TimedRotatingFileHandler
import logging

class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'DEBUG'

def get_logger():
    return current_app.logger

def set_logger_params(app):
    f = DebugFilter()
    debug_handler = TimedRotatingFileHandler(app.config['LOG_FILE_DEBUG'], when='D', interval=1)
    debug_handler.addFilter(f)
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(debug_handler)

    handler = TimedRotatingFileHandler(app.config['LOG_FILE'], when='D', interval=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(app.config['LOG_FORMAT']))
    app.logger.addHandler(handler)

