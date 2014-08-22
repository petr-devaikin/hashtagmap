import os
from htmapp.web.application_factory import create_app, init_app
import unittest
import tempfile
from htmapp.db.create import init_database

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test_config')
        self.db_fd, self.app.config['TEST_DATABASE'] = tempfile.mkstemp()
        init_app(self.app)
        with self.app.test_request_context():
            init_database()

    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.app.config['TEST_DATABASE'])
        #os.remove(app.config['LOG_FILE'])

    def test_location_urls(self):
        from htmapp.db.models.location import Location
        for location in Location.select():
            rv = self.app.test_client().get('/' + location.name)
            assert rv.status_code == 200

    def test_root_redirect(self):
        from htmapp.db.models.location import Location
        rv = self.app.test_client().get('/')
        assert rv.status_code == 302
        assert rv.headers['Location'].split('/')[-1] == Location.get().name

if __name__ == '__main__':
    unittest.main()