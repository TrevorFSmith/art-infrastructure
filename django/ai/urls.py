from django.contrib import admin
from django.conf.urls import url
from django.conf.urls import include

import weather.views as weather_views

urlpatterns = [

    url(r'^api/weather/icao-airport/(?P<airport_code>[^/]+).txt$', weather_views.icao_airport_observation, name='weather_icao'),
    url(r'^admin/', admin.site.urls),
    url(r'^heartbeat/', include('heartbeat.urls', namespace='heartbeat')),
    url(r'^lighting/', include('lighting.urls', namespace='lighting')),
    url(r'^iboot/', include('iboot.urls', namespace='iboot')),
    url(r'^artwork/', include('artwork.urls', namespace='artwork')),
    url(r'^', include('front.urls', namespace='front')),

    # url(r'^', include('account.api_urls', namespace='account_api')),

    url(r'^api/lighting/', include('lighting.api_urls', namespace='lighting_api')),
    url(r'^api/iboot/', include('iboot.api_urls', namespace='iboot_api')),
    url(r'^api/artwork/', include('artwork.api_urls', namespace='artwork_api')),
]
