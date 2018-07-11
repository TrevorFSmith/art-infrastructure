from rest_framework import serializers
from artwork import models
from lighting.models import BACNetLight
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

class ArtistSerializer(serializers.ModelSerializer):
    groups_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        ordering = ['name']
        model = models.Artist
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "artistgroup_set",
            "groups_info",
            "url",
            "notes",
            "created",
            ]

    def get_groups_info(self, obj):
        return obj.artistgroup_set.values("id", "name")


class ArtistGroupSerializer(serializers.ModelSerializer):
    artists_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        ordering = ['name']
        model = models.ArtistGroup
        fields = [
            "id",
            "name",
            "artists",
            "artists_info",
            "url",
            "created",
            ]

    def get_artists_info(self, obj):
        return obj.artists.values("id", "name")


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-created']
        model = models.Photo
        fields = [
            "id",
            "image",
            "title",
            "caption",
            "description",
            "created",
            ]


class EquipmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['name']
        model = models.EquipmentType
        fields = [
            "id",
            "name",
            "provider",
            "url",
            "notes",
            "created",
            ]


class EquipmentSerializer(serializers.ModelSerializer):
    equipment_type_name = serializers.SerializerMethodField(read_only=True)
    photos_info = serializers.SerializerMethodField(read_only=True)
    device_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        verbose_name_plural = 'equipment'
        ordering = ['name']
        model = models.Equipment
        fields = [
            "id",
            "name",
            "equipment_type",
            "equipment_type_name",
            "photos",
            "photos_info",
            "notes",
            "device_type",
            "device_id",
            "device_info",
            "created",
            ]

    def get_equipment_type_name(self, obj):
        if obj.equipment_type:
            return obj.equipment_type.name
        return ""

    def get_photos_info(self, obj):
        return obj.photos.values("id", "image", "title")

    def get_device_info(self, obj):
        if obj.device_type and obj.device_id:
          try:
            device = obj.device_type.get_object_for_this_type(pk=obj.device_id)
            device_info = {
              "id": device.id,
              "name": device.name,
              "status": device.status,
              "type": obj.device_type.name,
            }
            return device_info
          except obj.device_type.model_class().DoesNotExist:
            raise ObjectDoesNotExist("%s matching query does not exist." % obj.device_type.model_class()._meta.object_name)
        return ""


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-created']
        model = models.Document
        fields = [
            "id",
            "title",
            "doc",
            "created",
            ]


class InstallationSiteSerializer(serializers.ModelSerializer):
    photos_info = serializers.SerializerMethodField(read_only=True)
    equipment_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        verbose_name = 'location'
        verbose_name_plural = 'locations'
        ordering = ['name']
        model = models.InstallationSite
        fields = [
            "id",
            "name",
            "location",
            "notes",
            "photos",
            "photos_info",
            "equipment",
            "equipment_info",
            "created",
            ]

    def get_photos_info(self, obj):
        return obj.photos.values("id", "image", "title")

    def get_equipment_info(self, obj):
        return obj.equipment.values("id", "name")


class InstallationSerializer(serializers.ModelSerializer):
    site_name = serializers.SerializerMethodField(read_only=True)
    groups_info = serializers.SerializerMethodField(read_only=True)
    artists_info = serializers.SerializerMethodField(read_only=True)
    users_info = serializers.SerializerMethodField(read_only=True)
    photos_info = serializers.SerializerMethodField(read_only=True)
    documents_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        verbose_name =  'artwork'
        verbose_name_plural = 'works of art'
        ordering = ['name']
        model = models.Installation
        fields = [
            "id",
            "name",
            "groups",
            "artists",
            "user",
            "site",
            "opened",
            "closed",
            "notes",
            "photos",
            "documents",
            "created",
            "site_name",
            "groups_info",
            "artists_info",
            "users_info",
            "photos_info",
            "documents_info",
            ]

    def get_site_name(self, obj):
        if obj.site:
            return obj.site.name
        return ""

    def get_groups_info(self, obj):
        return obj.groups.values("id", "name")

    def get_artists_info(self, obj):
        return obj.artists.values("id", "name")

    def get_users_info(self, obj):
        return obj.user.values("id", "username")

    def get_photos_info(self, obj):
        return obj.photos.values("id", "image", "title")

    def get_documents_info(self, obj):
        return obj.documents.values("id", "doc", "title")


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        ordering = ['username']
        model = User
        fields = [
            "id",
            "name",
            ]


class SystemStatusSerializer(serializers.ModelSerializer):
    site_name = serializers.SerializerMethodField(read_only=True)
    equipment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        ordering = ['name']
        model = models.Installation
        fields = [
            "id",
            "name",
            "site_name",
            "equipment",
            ]

    def get_site_name(self, obj):
        if obj.site:
            return obj.site.name
        return ""

    def get_equipment(self, obj):
        if obj.site:
            exclude_device_type = ContentType.objects.get_for_model(BACNetLight)
            serializer = EquipmentSerializer(data=obj.site.equipment.exclude(device_type=exclude_device_type), many=True)
            serializer.is_valid()
            return serializer.data
        return []
