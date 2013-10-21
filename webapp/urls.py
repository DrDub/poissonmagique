from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = \
    patterns('',
             url(r'^$', 'webapp.views.home', name='home'),
             url(r'^msg/all$', 'webapp.poissonmagique.views.msg_all'),
             url(r'^msg/pending$', 'webapp.poissonmagique.views.msg_pending'),
             url(r'^msg/new$', 'webapp.poissonmagique.views.msg_new'),
             url(r'^msg/(?P<msg_id>.+)$', 'webapp.poissonmagique.views.msg', name='msg'),
             url(r"^account/", include("account.urls")),
             url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
             url(r'^admin/', include(admin.site.urls)),
             # url(r'^webapp/', include('webapp.foo.urls')),
             )
