from django.conf.urls import url

from iboot.api.v1 import views as views_v1

urlpatterns = [
    url(r'^v1/iboots/$', views_v1.IBootViewSet.as_view(), name='iboots'),
    url(r'^v1/iboots/(?P<paginate>\w+)/$', views_v1.IBootViewSet.as_view(), name='iboots'),
    url(r'^v1/iboots/command/$', views_v1.IBootCommandViewSet.as_view(), name='iboots_command'),
]
