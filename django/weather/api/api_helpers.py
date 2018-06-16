from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication


class ArtStaffApiPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user and (user.is_superuser or user.is_staff)


class GenericApiEndpoint(APIView):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (permissions.BasePermission, ArtStaffApiPermission)

    def __get_object(self, pk):
        pass