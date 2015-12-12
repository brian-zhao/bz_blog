from google.appengine.ext import ndb
from google.appengine.api import images


class Blog(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    body = ndb.BlobProperty(required=True)
    posted = ndb.DateProperty(auto_now_add=True)
    author = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty(required=False)
    thumnail = ndb.ComputedProperty(lambda self: images.get_serving_url(self.blob_key, size=32) if self.blob_key else '')

    @classmethod
    def query_blog(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.posted)


class Test(ndb.Model):
    test_int = ndb.IntegerProperty()
    test_float = ndb.FloatProperty()
    test_bool = ndb.BooleanProperty()
    test_datetime = ndb.DateTimeProperty()
    test_geo = ndb.GeoPtProperty()
    test_user = ndb.UserProperty()
    test_json = ndb.JsonProperty(compressed=True)
    test_pickle = ndb.PickleProperty()
    test_generic = ndb.GenericProperty()
    test_computed = ndb.ComputedProperty(lambda self: self.user.name.lower())
