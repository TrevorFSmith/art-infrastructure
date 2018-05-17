from lighting import models
from rest_framework import permissions, pagination
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication

class ArtStaffApiPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user and (user.is_superuser or user.is_staff)


class GenericApiEndpoint(APIView, pagination.PageNumberPagination):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.BasePermission, ArtStaffApiPermission)

    page_size = 9

    def get_queryset(self, request):
        collection = self.get_queryset_class.objects.all()
        return self.paginate_queryset(collection, self.request)


    def get(self, request, format=None):
        serializer = self.get_queryset_serializer_class(self.get_queryset(request), many=True)
        return self.get_paginated_response(serializer.data)


    def __get_object(self, pk):
        pass
