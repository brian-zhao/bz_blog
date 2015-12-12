import cgi
import datetime
from os import path

from django.shortcuts import render
from django.http import HttpResponseRedirect

from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore

from blog.models import Blog
# from identitytoolkit import gitkitclient


# server_config_json = path.join(path.dirname(path.realpath(__file__)), 'gitkit-server-config.json')
# gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(server_config_json)


def home(request):
    blogs = ndb.gql("SELECT * FROM Blog ORDER BY posted DESC")
    return render(request, "blog/index.html", {'blogs': blogs, })


def blog(request, idx):
    blog_key = ndb.Key('Blog', int(idx))
    blog = blog_key.get()
    image_url = images.get_serving_url(blog.blob_key) if blog.blob_key else ''
    return render(request, "blog/blog.html", {'blog': blog, 'image_url': image_url})


def signin(request):
    return render(request, 'blog/widget.html')


def create_blog(request):
    if request.method == 'POST':
        items = request.POST
        b = Blog(title=items['title'], slug=items['slug'], body=str(items['body']))
        b.posted = datetime.datetime.now().date()

        # if 'gtoken' in request.cookies:
        #     gitkit_user = gitkit_instance.VerifyGitkitToken(request.cookies['gtoken'])
        #     if gitkit_user:
        #         b.author = gitkit_user.email

        if get_uploads(request, 'image'):
            blob_key = get_uploads(request, 'image')[0].key()
            b.blob_key = blob_key
        b.put()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'blog/create_blog.html', {'upload_url': blobstore.create_upload_url(success_path='/create_blog')})


def get_uploads(request, field_name=None, populate_post=False):
    if hasattr(request, '__uploads') == False:
        request.META['wsgi.input'].seek(0)
        fields = cgi.FieldStorage(
            request.META['wsgi.input'], environ=request.META)

        request.__uploads = {}
        if populate_post:
            request.POST = {}

        for key in fields.keys():
            field = fields[key]
            if isinstance(field, cgi.FieldStorage) and \
                        'blob-key' in field.type_options:
                request.__uploads.setdefault(key, []).append(
                    blobstore.parse_blob_info(field))
            elif populate_post:
                request.POST[key] = field.value

    if field_name:
        try:
            return list(request.__uploads[field_name])
        except KeyError:
            return []
    else:
        results = []
        for uploads in request.__uploads.itervalues():
            results += uploads
        return results
