from django.conf.urls import url

import views

urlpatterns = [
    url(r'^artists/$', views.ArtistViewSet.as_view(), name='artists'),
    url(r'^artist_groups/$', views.ArtistGroupViewSet.as_view(), name='artist_groups'),
    url(r'^photos/$', views.PhotoViewSet.as_view(), name='photos'),
    url(r'^documents/$', views.DocumentViewSet.as_view(), name='documents'),
    url(r'^equipment_types/$', views.EquipmentTypeViewSet.as_view(), name='equipment_types'),
    url(r'^equipments/$', views.EquipmentViewSet.as_view(), name='equipments'),
    url(r'^installation_sites/$', views.InstallationSiteViewSet.as_view(), name='installation_sites'),
    url(r'^installations/$', views.InstallationViewSet.as_view(), name='installations'),
    url(r'^system_status/$', views.SystemStatusViewSet.as_view(), name='system_status'),
]