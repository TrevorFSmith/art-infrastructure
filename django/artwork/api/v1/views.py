from artwork import serializers, models
from artwork.api import api_helpers
from rest_framework.response import Response
from rest_framework import status


class ArtistViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Artist
    get_queryset_serializer_class = serializers.ArtistSerializer

    def post(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "artistgroup_set")
        serializer = serializers.ArtistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "artistgroup_set")
        try:
            get_object = models.Artist.objects.get(pk=int(data.get("id")))
            serializer = serializers.ArtistSerializer(get_object, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


class ArtistGroupViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.ArtistGroup
    get_queryset_serializer_class = serializers.ArtistGroupSerializer

    def post(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "artists")
        serializer = serializers.ArtistGroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "artists")
        try:
            get_object = models.ArtistGroup.objects.get(pk=int(data.get("id")))
            serializer = serializers.ArtistGroupSerializer(get_object, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


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