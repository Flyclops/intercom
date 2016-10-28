from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.views import serve
from .views import entry_point, authenticate_member

urlpatterns = patterns('',
    url(r'^first_contact$', entry_point, name='entry_point'),
    url(r'^authenticate$', authenticate, name='authenticate'),
    url(r'^authenticate_member$', authenticate_member, name='authenticate_member'),
    url(r'^(?P<path>voice/.*)$', serve),
)
