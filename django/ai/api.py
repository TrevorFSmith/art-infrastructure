from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.settings import api_settings


class NoPermission(permissions.BasePermission):
    '''
    Use this on APIViews that do not require authentication of any kind
    '''
    def has_permission(self, request, view):
        return True


class ActiveAndAuthenticatedPermission(permissions.BasePermission):
    '''
    Use this on APIViews that require an authenticated User who also is_active
    '''
    def has_permission(self, request, view):
        if request.user.is_anonymous(): return False
        return request.user.is_active


class StaffPermission(permissions.BasePermission):
    '''
    Use this on APIViews that require an authenticated User who is active and a staff member
    '''
    def has_permission(self, request, view):
        if request.user.is_anonymous(): return False
        if not request.user.is_active: return False
        return request.user.is_staff

class PaginatedAPIView(APIView):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            self._paginator = self.pagination_class()
        return self._paginator
