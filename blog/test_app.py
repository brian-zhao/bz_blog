import unittest
from webtest import TestApp

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from bz_blog.wsgi import application
from blog.models import Blog


class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()
        self.app = TestApp(application)

    def tearDown(self):
        self.testbed.deactivate()

    def testFetchRootURL(self):
        result = self.app.get('/')
        self.assertEqual(result.status, '200 OK')

    def testBlogEntry(self):
        tb = Blog(title='KEIFJUE', slug='PDEMDKS', body='MDOWMF')
        tb.put()
        result = self.app.get('/')
        self.assertIn('KEIFJUE', result.body)
        self.assertIn('MDOWMF', result.body)

    def testQueryBlog(self):
        tb = Blog(title='abc', slug='abc', body='abc')
        tb_key = tb.put()
        qry = Blog.query_blog(tb_key)
        result = qry.fetch()
        self.assertEqual('abc', result[0].body)

    def testSort(self):
        tb1 = Blog(title='first', slug='first', body='first')
        tb1.put()

        tb2 = Blog(title='second', slug='second', body='second')
        tb2.put()

        self.assertEqual('second', Blog.query().order(-Blog.posted).fetch(1)[0].title)
