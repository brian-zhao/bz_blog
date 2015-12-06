from django.db import models
from google.appengine.ext import db
from google.appengine.api import users
import webapp2
import datetime

class Blog(models.Model):
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body = db.StringProperty(required=True)
    posted = db.DateProperty()
    author = db.StringProperty()

    meta = {
        'indexes': [
            'title',
            'slug'
        ]
    }
