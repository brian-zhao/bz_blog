import datetime
import random

from django.shortcuts import render
from django.http import HttpResponseRedirect
from google.appengine.ext import db

from blog.models import Blog


def home(request):
    blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY posted")
    return render(request, "blog/index.html", {'blogs': blogs})


def blog(request, idx):
    blogs = db.GqlQuery("SELECT * FROM Blog WHERE idx = :1", idx)
    return render(request, "blog/blog.html", {'blogs': blogs})


def create_blog(request):
    if request.method == 'POST':
        items = request.POST
        b = Blog(title=items['title'], slug=items['slug'], body=items['body'])
        b.posted = datetime.datetime.now().date()
        b.author = ''
        b.idx = str(random.getrandbits(32))
        b.put()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'blog/create_blog.html')
