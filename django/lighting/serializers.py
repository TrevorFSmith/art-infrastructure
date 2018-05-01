from rest_framework import serializers
from lighting import models


class ProjectorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Projector
        fields = [
            "id",
            "name",
            "pjlink_host",
            "pjlink_port",
            "pjlink_password"
            ]


class BACNetLightSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.BACNetLight
        fields = [
            "id",
            "name",
            "device_id",
            "property_id",
            ]
