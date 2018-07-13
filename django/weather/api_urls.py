from django.conf.urls import url
from weather.api.v1 import views as views_v1


"""
Note that there is this new JSON based weather API
The old text weather API is in weather.views.icao_airport_observation
"""
urlpatterns = [
    url(r'^v1/icao-airport/(?P<airport_code>[^/]+)$', views_v1.WeatherViewSet.as_view(), name='weather'),
]
