from django.conf.urls import patterns, include, url
from django.contrib import admin
import intercom.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include(intercom.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
