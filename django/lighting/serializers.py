from rest_framework import serializers
from lighting import models
import pjlink


class ProjectorSerializer(serializers.HyperlinkedModelSerializer):

    commands = serializers.SerializerMethodField()

    class Meta:
        ordering = ['name']
        model = models.Projector
        fields = [
            "id",
            "name",
            "pjlink_host",
            "pjlink_port",
            "pjlink_password",
            "commands",
            ]

    def get_commands(self, obj):
        return [
            {
                "title": "Power Off",
                "command": pjlink.PJLinkProtocol.POWER_OFF_STATUS,
            },
            {
                "title": "Power On",
                "command": pjlink.PJLinkProtocol.POWER_ON_STATUS,
            }]


class ProjectorEventsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.ProjectorEvent
        fields = [
            "id",
            "command",
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

class CrestonSerializer(serializers.HyperlinkedModelSerializer):

    commands = serializers.SerializerMethodField()

    class Meta:
        ordering = ['name']
        model = models.Creston
        fields = [
            "id",
            "name",
            "host",
            "port",
            "commands",
            ]

    def get_commands(self, obj):
        return [
            {
                "title": "Ping",
                "command": "Ping",
            },
            {
                "title": "Query system",
                "command": "Update",
            }]
