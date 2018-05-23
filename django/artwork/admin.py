from django.contrib import admin
from django import forms

from models import (
    Document,
    ArtistGroup,
    Artist,
    Photo,
    Equipment,
    EquipmentType,
    InstallationSite,
    Installation
)

from ai.admin import StyledModelAdmin

class DocumentAdmin(StyledModelAdmin):
    list_display = ('title', 'doc', 'created')
admin.site.register(Document, DocumentAdmin)

class ArtistGroupAdmin(StyledModelAdmin):
    filter_horizontal = ('artists',)
admin.site.register(ArtistGroup, ArtistGroupAdmin)

class ArtistAdmin(StyledModelAdmin):
    pass
admin.site.register(Artist, ArtistAdmin)

class PhotoAdmin(StyledModelAdmin):
    list_display = ('display_name', 'image')
    search_fields = ('title', 'image')
admin.site.register(Photo, PhotoAdmin)

class EquipmentTypeAdmin(StyledModelAdmin):
    pass
admin.site.register(EquipmentType, EquipmentTypeAdmin)

class EquipmentAdmin(StyledModelAdmin):
    filter_horizontal = ('photos',)
admin.site.register(Equipment, EquipmentAdmin)

class InstallationSiteAdmin(StyledModelAdmin):
    filter_horizontal = ('photos', 'equipment')
admin.site.register(InstallationSite, InstallationSiteAdmin)

class InstallationAdmin(StyledModelAdmin):
    list_display = ('name', 'site', 'is_opened')
    filter_horizontal = ('artists', 'groups', 'photos')
admin.site.register(Installation, InstallationAdmin)
