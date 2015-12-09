import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect

from google.appengine.ext import ndb
from google.appengine.api import images

from blog.models import Blog


def home(request):
    blogs = ndb.gql("SELECT * FROM Blog ORDER BY posted")
    return render(request, "blog/index.html", {'blogs': blogs})


def blog(request, idx):
    blog_key = ndb.Key('Blog', int(idx))
    blog = blog_key.get()
    return render(request, "blog/blog.html", {'blog': blog})


def create_blog(request):
    if request.method == 'POST':
        items = request.POST
        b = Blog(title=items['title'], slug=items['slug'], body=items['body'])
        b.posted = datetime.datetime.now().date()
        b.author = ''

        if request.FILES.get('image'):
            b.image = request.FILES['image'].read()
            b.serving_url = images.get_serving_url(request.FILES['image'].name)
        b.put()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'blog/create_blog.html')
