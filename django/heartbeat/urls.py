from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

from heartbeat import views

urlpatterns = [
    #
    # TODO: use class based view
    #
    url(r'^$', views.index, name='index'),
]
