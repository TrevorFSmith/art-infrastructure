from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import TemplateView
from api.api_helpers import ArtStaffApiPermission


class GenericAdmitArtView(PermissionRequiredMixin, TemplateView):
    permission_classes = (ArtStaffApiPermission,)
    permission_required = ()


class BACNetViewSet(GenericAdmitArtView):
    template_name = 'lighting/bacnet_lights.html'


class ProjectorViewSet(GenericAdmitArtView):
    template_name = 'lighting/projectors.html'


class CrestonViewSet(GenericAdmitArtView):
    template_name = 'lighting/crestons.html'
