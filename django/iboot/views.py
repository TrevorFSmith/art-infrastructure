from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import TemplateView
from api.api_helpers import ArtStaffApiPermission


class GenericAdmitArtView(PermissionRequiredMixin, TemplateView):
    permission_classes = (ArtStaffApiPermission,)
    permission_required = ()

class IBootViewSet(GenericAdmitArtView):
    template_name = 'iboot/iboots.html'