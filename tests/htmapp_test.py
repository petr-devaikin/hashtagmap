import os
from htmapp.web.application_factory import create_app, init_app
import unittest
import tempfile
from htmapp.db.create import init_database

class FlaskrTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.app = create_app('test_config')
        self.db_fd, self.app.config['TEST_DATABASE'] = tempfile.mkstemp()
        init_app(self.app)
        with self.app.test_request_context():
            init_database()

    @classmethod
    def tearDownClass(self):
        os.close(self.db_fd)
        os.remove(self.app.config['TEST_DATABASE'])
        #os.remove(app.config['LOG_FILE'])


    def test_database_recreate(self):
        with self.app.test_request_context():
            init_database()


    def test_location_urls(self):
        from htmapp.db.models.location import Location
        for location in Location.select():
            rv = self.app.test_client().get('/' + location.name)
            self.assertEqual(rv.status_code, 200)

    def test_root_redirect(self):
        from htmapp.db.models.location import Location
        rv = self.app.test_client().get('/')
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.headers['Location'].split('/')[-1], Location.get().name)

    def test_update_tags(self):
        from htmapp.datagrabber.tags_updater import update_tags
        with self.app.test_request_context():
            print self.app.config['UPDATE_THREADS_COUNT']
            print self.app.config['TAGS_MEMORY']
            #update_tags(threads_count=self.app.config['UPDATE_THREADS_COUNT'],
            #    memory=self.app.config['TAGS_MEMORY'])


if __name__ == '__main__':
    unittest.main()