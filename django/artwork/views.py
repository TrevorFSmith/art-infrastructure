from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import TemplateView
from api.api_helpers import ArtStaffApiPermission


class GenericAdmitArtView(PermissionRequiredMixin, TemplateView):
    permission_classes = (ArtStaffApiPermission,)
    permission_required = ()


class ArtistViewSet(GenericAdmitArtView):
    template_name = 'artwork/artists.html'


class ArtistGroupViewSet(GenericAdmitArtView):
    template_name = 'artwork/artist_groups.html'


class PhotoViewSet(GenericAdmitArtView):
    template_name = 'artwork/photos.html'


class DocumentViewSet(GenericAdmitArtView):
    template_name = 'artwork/documents.html'


class EquipmentTypeViewSet(GenericAdmitArtView):
    template_name = 'artwork/equipment_types.html'


class EquipmentViewSet(GenericAdmitArtView):
    template_name = 'artwork/equipments.html'


class InstallationSiteViewSet(GenericAdmitArtView):
    template_name = 'artwork/installation_sites.html'


class InstallationViewSet(GenericAdmitArtView):
    template_name = 'artwork/installations.html'


class SystemStatusViewSet(GenericAdmitArtView):
    template_name = 'artwork/system_status.html'