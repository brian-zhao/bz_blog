from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body = db.StringProperty(required=True)
    posted = db.DateProperty()
    author = db.StringProperty()
    idx = db.StringProperty()

    meta = {
        'indexes': [
            'title',
            'slug',
            'posted',
            'idx'
        ]
    }
