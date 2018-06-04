from rest_framework import serializers
from artwork import models


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
            "created",
            ]

    def get_equipment_type_name(self, obj):
        return obj.equipment_type.name

    def get_photos_info(self, obj):
        return obj.photos.values("id", "image", "title")


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        ordering = ['-created']
        model = models.Document
        fields = [
            "id",
            "title",
            "doc",
            "created",
            ]


class InstallationSiteSerializer(serializers.HyperlinkedModelSerializer):

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
            "equipment",
            "created",
            ]


class InstallationSerializer(serializers.HyperlinkedModelSerializer):

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
            ]