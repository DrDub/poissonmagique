from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = \
    patterns('',
             url(r'^$', 'webapp.views.home', name='home'),
             url(r"^account/", include("account.urls")),
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             url(r'^admin/', include(admin.site.urls)),
             url(r'', include('webapp.poissonmagique.urls')),
             )
