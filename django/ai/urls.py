from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
import artwork.views as artwork_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lighting/', include('lighting.urls', namespace='lighting')),
    url(r'^iboot/', include('iboot.urls', namespace='iboot')),
    url(r'^artwork/', include('artwork.urls', namespace='artwork')),
    url(r'^$', artwork_views.SystemStatusViewSet.as_view(), name="system_status"),

    # url(r'^', include('account.api_urls', namespace='account_api')),

    url(r'^api/lighting/', include('lighting.api_urls', namespace='lighting_api')),
    url(r'^api/iboot/', include('iboot.api_urls', namespace='iboot_api')),
    url(r'^api/artwork/', include('artwork.api_urls', namespace='artwork_api')),
    url(r'^api/weather/', include('weather.api_urls', namespace='weather_api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
