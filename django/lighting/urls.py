from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
	url(r'^bnlight/(?P<id>[\d]+)/$', views.bacnet_light, name='bacnet_light'),
	url(r'^projector/(?P<id>[\d]+)/$', views.projector, name='projector'),
	url(r'^creston/$', views.creston, name='creston'),
	url(r'^$', views.index, name='index'),
]
