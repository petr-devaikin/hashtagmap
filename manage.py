# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from htmapp.web.app import app
#from htm.database import init_db

manager = Manager(app)

@manager.command
def hello():
    """
    Print hello
    """
    print "hello"

@manager.command
def init_db():
    """
    Drop and create database
    """
    init_db()

@manager.command
def update_tags():
    """
    Update tags in database
    """
    from htm.datagrabber.tags_updater import update_tags
    update_tags(threads_count=100, memory=24 * 3600)

if __name__ == "__main__":
    manager.run()