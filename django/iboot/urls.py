from django.conf.urls import url

import views

urlpatterns = [
    url(r'^iboots/$', views.IBootViewSet.as_view(), name='iboots'),
]