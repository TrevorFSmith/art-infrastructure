from artwork import serializers, models
from artwork.api import api_helpers


class ArtistViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Artist
    get_queryset_serializer_class = serializers.ArtistSerializer


class ArtistGroupViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.ArtistGroup
    get_queryset_serializer_class = serializers.ArtistGroupSerializer


class PhotoViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Photo
    get_queryset_serializer_class = serializers.PhotoSerializer


class DocumentViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Document
    get_queryset_serializer_class = serializers.DocumentSerializer


class EquipmentTypeViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.EquipmentType
    get_queryset_serializer_class = serializers.EquipmentTypeSerializer


class EquipmentViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Equipment
    get_queryset_serializer_class = serializers.EquipmentSerializer


class InstallationSiteViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.InstallationSite
    get_queryset_serializer_class = serializers.InstallationSiteSerializer


class InstallationViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Installation
    get_queryset_serializer_class = serializers.InstallationSerializer


class SystemStatusViewSet(api_helpers.GenericApiEndpoint):
    pass