from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    url(r'^first_contact$', views.entry_point, name='entry_point'),
    url(r'^authenticate_member$', views.authenticate_member, name='authenticate_member'),
)
