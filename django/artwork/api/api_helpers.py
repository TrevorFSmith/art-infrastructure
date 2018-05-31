from rest_framework import permissions, pagination
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

class ArtStaffApiPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user and (user.is_superuser or user.is_staff)


class GenericApiEndpoint(APIView, pagination.PageNumberPagination):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.BasePermission, ArtStaffApiPermission)

    page_size = 9

    def get_queryset(self, request):
        if not request.data:
          collection = self.get_queryset_class.objects.all()
        else:
          collection = self.get_queryset_class.objects.filter(pk__in=request.data)
        return self.paginate_queryset(collection, self.request)


    def get(self, request, format=None):
        serializer = self.get_queryset_serializer_class(self.get_queryset(request), many=True)
        return self.get_paginated_response(serializer.data)


    def post(self, request, format=None):
        serializer = self.get_queryset_serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        try:
            get_object = self.get_queryset_class.objects.get(pk=int(request.data.get("id")))
            serializer = self.get_queryset_serializer_class(get_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise Http404


    def delete(self, request, format=None):
        try:
            get_object  = self.get_queryset_class.objects.get(pk=int(request.data.get("id")))
            object_id = get_object.id
            get_object.delete()
        except (ObjectDoesNotExist, TypeError):
            raise Http404

        return Response({"id": object_id}, status=status.HTTP_200_OK)


    def __get_object(self, pk):
        pass


class Utils:

    @staticmethod
    def convert_request(request, field):
        data = request.data.copy()
        if data.has_key(field + "[]"):
          artists = data.getlist(field + "[]")
          data.setlist(field, artists)
        return data