from google.appengine.ext import ndb


class Blog(ndb.Model):
    title = ndb.StringProperty(required=True)
    slug = ndb.StringProperty(required=True)
    body = ndb.StringProperty(required=True)
    posted = ndb.DateProperty(auto_now_add=True)
    author = ndb.StringProperty()
    image = ndb.BlobProperty(default=None)
    serving_url = ndb.StringProperty(indexed=False)

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
