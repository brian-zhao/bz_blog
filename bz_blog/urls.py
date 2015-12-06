from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin
from django.views.generic import RedirectView
from blog.views import CreateUser

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^$',  RedirectView.as_view(url='/blog/')),
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('blog.urls')),
    (r'^accounts/create_user/$', CreateUser.as_view()),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm,
        'template_name': 'blog/login.html',}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/blog/',}),
)
