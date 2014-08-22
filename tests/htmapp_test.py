import os
from htmapp.web.app import app
import unittest
import tempfile
from htmapp.db.db_engine import init_db
from htmapp.db.create import init_database
from htmapp.logger import set_logger_params

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.config['TEST_DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['LOG_FILE'] = app.config['LOG_FILE_DEBUG'] = app.config['LOG_FILE_TEST']
        set_logger_params(app)
        with app.test_request_context():
        #self.client = app.test_client()
            init_db(app)
            init_database()

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(app.config['TEST_DATABASE'])
        os.remove(app.config['LOG_FILE_TEST'])

    def test_location_urls(self):
        from htmapp.db.models.location import Location
        for location in Location.select():
            rv = app.test_client().get('/' + location.name)
            assert rv.status_code == 200

    def test_root_redirect(self):
        from htmapp.db.models.location import Location
        rv = app.test_client().get('/')
        assert rv.status_code == 302
        assert rv.headers['Location'].split('/')[-1] == Location.get().name

if __name__ == '__main__':
    unittest.main()