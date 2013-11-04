from django.conf.urls import patterns, include, url
from views import new_roll, roll

urlpatterns = \
    patterns('',
             url(r'^new$', new_roll, name='dice_new'),
             url(r'^show/(?P<hash>[0-9]+)$', roll, { 'do_roll' : False }, name='dice_show'),
             url(r'^roll/(?P<hash>[0-9]+)$', roll, { 'do_roll' : True }, name='dice_roll')
             )
