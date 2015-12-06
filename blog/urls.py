from django.conf.urls import *
from blog.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^create_blog','blog.views.create_blog', name='create_blog'),
]


