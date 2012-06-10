from django.conf.urls import patterns, include, url
from django.contrib import admin
import intercom.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^', include(intercom.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
