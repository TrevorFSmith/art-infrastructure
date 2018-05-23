from django.conf.urls import url

import views

urlpatterns = [

    url(r'^bacnet_lights/$', views.BACNetViewSet.as_view(), name='bacnet_lights'),
    url(r'^projectors/$', views.ProjectorViewSet.as_view(), name='projectors'),
    url(r'^crestons/$', views.CrestonViewSet.as_view(), name='crestons'),

]
