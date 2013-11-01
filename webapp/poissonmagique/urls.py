from django.conf.urls import patterns, include, url
from views import msg_list, msg_new, msg

urlpatterns = \
    patterns('',
             url(r'^msg/all$', msg_list, { 'filter': False }, name='msg_all'),
             url(r'^msg/pending$', msg_list, { 'filter': False }, name='msg_pending'),
             url(r'^msg/new$', msg_new),
             url(r'^msg/(?P<msg_id>.+)$', msg, name='msg'),
    )
