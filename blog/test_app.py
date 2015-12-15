import unittest
from webtest import TestApp
from google.appengine.ext import testbed

from bz_blog.wsgi import application


class HomepageTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()

        self.testbed.setup_env(app_id='bzblog-1152')
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # create test server
        self.testapp = TestApp(application)

    def tearDown(self):
        self.testbed.deactivate()

    def testFetchRootURL(self):
        result = self.testapp.get('/')
        self.assertEqual(result.status, '200 OK')
