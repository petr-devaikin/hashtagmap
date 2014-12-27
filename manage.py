# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from htmapp.web.application_factory import create_app, init_app
from htmapp.logger import get_logger
from htmapp.db.scripts.create import init_database
from htmapp.datagrabber import tags_updater

app = create_app()
init_app(app)
manager = Manager(app)


@manager.command
def hello():
    """
    Print hello
    """
    get_logger().debug("Hello debug")
    get_logger().info("Hello info")
    get_logger().warning("Hello warning")
    get_logger().error("Hello error")
    get_logger().critical("Hello critical")
    print "hello"


@manager.command
def init_db():
    """
    Drop and create database
    """
    init_database()


@manager.command
def add_spb():
    """
    Add Spb location
    """
    from htmapp.db.scripts.create_spb_location import create_spb_location
    create_spb_location()


@manager.command
def add_berlin():
    """
    Add Berlin location
    """
    from htmapp.db.scripts.create_berlin_location import create_berlin_location
    create_berlin_location()


@manager.command
def update_tags():
    """
    Update tags in database
    """
    tags_updater.update_tags(app.config['REQUEST_THREADS_COUNT'],
                             app.config['SUMMARIZE_THREADS_COUNT'],
                             app.config['TAGS_MEMORY'])


if __name__ == "__main__":
    manager.run()
