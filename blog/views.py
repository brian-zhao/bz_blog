import cgi
from os import path

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages

from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore

from blog.models import Blog
from identitytoolkit import gitkitclient


gitkit = gitkitclient.GitkitClient(
    client_id='272073482545-snlclt17idhchcurcc46vs592kbugt22.apps.googleusercontent.com',
    service_account_email='account@bzblog-1152.iam.gserviceaccount.com',
    service_account_key=path.join(path.dirname(path.realpath(__file__)), 'private-ke.p12'),
    cookie_name='gtoken')


def home(request):
    blogs = Blog.query().order(-Blog.posted)
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
        if not items['title'] or not items['slug'] or items['body']:
            messages.error(request, 'Title, Slug, Body are required fields.')
            return redirect('create_blog')

        b = Blog(title=items['title'], slug=items['slug'], body=str(items['body']))

        if 'gtoken' in request.COOKIES:
            gitkit_user = gitkit.VerifyGitkitToken(request.COOKIES['gtoken'])
            if gitkit_user:
                b.author = gitkit_user.email

        if get_uploads(request, 'image') and request.FILES.get('image'):
            blob_key = get_uploads(request, 'image')[0].key()
            b.blob_key = blob_key

        b.put()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'blog/create_blog.html', {'upload_url': blobstore.create_upload_url(success_path='/create_blog')})


def get_uploads(request, field_name=None, populate_post=False):
    """
    http://appengine-cookbook.appspot.com/recipe/blobstore-get_uploads-helper-function-for-django-request/

    Get uploads sent to this handler.

    Args:
    field_name: Only select uploads that were sent as a specific field.
    populate_post: Add the non blob fields to request.POST

    Returns:
    A list of BlobInfo records corresponding to each upload.
    Empty list if there are no blob-info records for field_name.
    """

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
