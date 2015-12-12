from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^blog/(?P<idx>\w{0,256})/$', 'blog.views.blog', name='blog_details'),
    url(r'^create_blog','blog.views.create_blog', name='create_blog'),
    url(r'^widget','blog.views.signin', name='signin'),

    url(r'^admin/', include(admin.site.urls)),
    # (r'^accounts/create_user/$', CreateUser.as_view()),
    # (r'^accounts/login/$', 'django.contrib.auth.views.login',
    #     {'authentication_form': AuthenticationForm,
    #     'template_name': 'blog/login.html',}),
    # (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
    #     {'next_page': '/blog/',}),
)
