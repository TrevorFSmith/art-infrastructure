from rest_framework import serializers
from iboot import models


class IBootSerializer(serializers.HyperlinkedModelSerializer):

    commands = serializers.SerializerMethodField()

    class Meta:
        ordering = ['name']
        model = models.IBootDevice
        fields = [
            "id",
            "name",
            "mac_address",
            "host",
            "port",
            "commands",
            ]

    def get_commands(self, obj):
        return [
            {
                "title": "Cycle",
                "command": "cycle",
            },
            {
                "title": "Turn On",
                "command": "on",
            },
            {
                "title": "Turn Off",
                "command": "off",
            },
            {
                "title": "Toggle",
                "command": "toggle",
            }]


class IBootEventsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.IBootEvent
        fields = [
            "id",
            "command",
            ]