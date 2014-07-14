# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from htmapp.web.app import app

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
    from htmapp.db.create import init_database
    init_database()

@manager.command
def update_tags():
    """
    Update tags in database
    """
    from htmapp.datagrabber.tags_updater import update_tags
    update_tags(threads_count=100, memory=24 * 3600)

if __name__ == "__main__":
    manager.run()