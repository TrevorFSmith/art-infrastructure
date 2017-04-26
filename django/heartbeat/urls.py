from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

import heartbeat.views as heartbeat_views 

urlpatterns = [
	url(r'^$', heartbeat_views.index, name='index'),
]
