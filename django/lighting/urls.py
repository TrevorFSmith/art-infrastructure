from django.conf.urls import url

import views

urlpatterns = [
    url(r'^bacnet_lights/$', views.bacnet_lights, name='bacnet_lights'),
    url(r'^projectors/$', views.projectors, name='projectors'),
    url(r'^crestons/$', views.crestons, name='crestons'),
]
