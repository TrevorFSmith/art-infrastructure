from artwork import serializers, models
from artwork.api import api_helpers
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User


class ArtistViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Artist
    get_queryset_serializer_class = serializers.ArtistSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(ArtistViewSet, self).get(request, format)
        else:
            artists = models.Artist.objects.all()
            serializer = serializers.ArtistSerializer(artists, many=True)
            return Response(serializer.data)

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

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(ArtistGroupViewSet, self).get(request, format)
        else:
            artist_groups = models.ArtistGroup.objects.all()
            serializer = serializers.ArtistGroupSerializer(artist_groups, many=True)
            return Response(serializer.data)


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

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(PhotoViewSet, self).get(request, format)
        else:
            photos = models.Photo.objects.all()
            serializer = serializers.PhotoSerializer(photos, many=True)
            return Response(serializer.data)


class DocumentViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Document
    get_queryset_serializer_class = serializers.DocumentSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(DocumentViewSet, self).get(request, format)
        else:
            documents = models.Document.objects.all()
            serializer = serializers.DocumentSerializer(documents, many=True)
            return Response(serializer.data)


class EquipmentTypeViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.EquipmentType
    get_queryset_serializer_class = serializers.EquipmentTypeSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(EquipmentTypeViewSet, self).get(request, format)
        else:
            equipment_types = models.EquipmentType.objects.all()
            serializer = serializers.EquipmentTypeSerializer(equipment_types, many=True)
            return Response(serializer.data)


class EquipmentViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Equipment
    get_queryset_serializer_class = serializers.EquipmentSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(EquipmentViewSet, self).get(request, format)
        else:
            equipment_types = models.Equipment.objects.all()
            serializer = serializers.EquipmentSerializer(equipment_types, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "photos")
        serializer = serializers.EquipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "photos")
        try:
            get_object = models.Equipment.objects.get(pk=int(data.get("id")))
            serializer = serializers.EquipmentSerializer(get_object, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


class InstallationSiteViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.InstallationSite
    get_queryset_serializer_class = serializers.InstallationSiteSerializer

    def get(self, request, format=None, paginate="on"):
        if paginate == "on":
            return super(InstallationSiteViewSet, self).get(request, format)
        else:
            installation_sites = models.InstallationSite.objects.all()
            serializer = serializers.InstallationSiteSerializer(installation_sites, many=True)
            return Response(serializer.data)


    def post(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "photos", "equipment")
        serializer = serializers.InstallationSiteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "photos", "equipment")
        try:
            get_object = models.InstallationSite.objects.get(pk=int(data.get("id")))
            serializer = serializers.InstallationSiteSerializer(get_object, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


class InstallationViewSet(api_helpers.GenericApiEndpoint):
    get_queryset_class            = models.Installation
    get_queryset_serializer_class = serializers.InstallationSerializer

    def post(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "groups", "artists", "user", "photos", "documents")
        serializer = serializers.InstallationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = api_helpers.Utils.convert_request(request, "groups", "artists", "user", "photos", "documents")
        try:
            get_object = models.Installation.objects.get(pk=int(data.get("id")))
            serializer = serializers.InstallationSerializer(get_object, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


class SystemStatusViewSet(api_helpers.GenericApiEndpoint):
    pass


class UserViewSet(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)
