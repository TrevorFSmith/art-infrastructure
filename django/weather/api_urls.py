from django.conf.urls import url
from weather.api.v1 import views as views_v1

urlpatterns = [
    url(r'^v1/icao-airport/(?P<airport_code>[^/]+).txt$', views_v1.WeatherViewSet.as_view(), name='weather'),
]
