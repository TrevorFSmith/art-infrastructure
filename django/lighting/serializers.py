from rest_framework import serializers
from lighting import models


class ProjectorSerializer(serializers.HyperlinkedModelSerializer):

    commands = serializers.SerializerMethodField()

    class Meta:
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
        return [{"title": tup[1], "command": tup[0]} for tup in models.ProjectorEvent.COMMAND_CHOICES]


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
