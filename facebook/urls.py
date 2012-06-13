from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^login/$', 'facebook.views.login', name="facebook_login"),
    url(r'^logout/$', 'facebook.views.logout', name="facebook_logout"),
    url(r'^callback/$', 'facebook.views.callback', name="facebook_callback"),
    url(r'^channel/$', direct_to_template, {"template": "facebook/channel.html",}, name="facebook_channel"),
)