import unittest
from webtest import TestApp

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from bz_blog.wsgi import application


class TestBlog(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    body = ndb.BlobProperty(required=True)
    posted = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty(required=False)
    thumnail = ndb.ComputedProperty(lambda self: images.get_serving_url(self.blob_key, size=32) if self.blob_key else '')

    @classmethod
    def query_blog(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.posted)


class DatastoreTestCase(unittest.TestCase):
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

    def tearDown(self):
        self.testbed.deactivate()

    def testInsertEntity(self):
        tb = TestBlog(title='a', slug='a', body='a')
        tb.put()
        self.assertEqual(1, len(TestBlog.query().fetch(2)))

    def testSort(self):
        tb1 = TestBlog(title='first', slug='first', body='first')
        tb1.put()

        tb2 = TestBlog(title='second', slug='second', body='second')
        tb2.put()

        self.assertEqual('second', TestBlog.query().order(-TestBlog.posted).fetch(1)[0].title)
