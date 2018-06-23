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
            "status",
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
            "status",
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
            "status",
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
            },
            # {
            #     "title": "For help with list of Commands",
            #     "command": "Help",
            # },
            {
                "title": "Dim On/Off Toggle",
                "command": "EnableDim",
            },
            {
                "title": "To adjust the Dim sensitivity up",
                "command": "DimLvlUp",
            },
            {
                "title": "To adjust the Dim sensitivity down",
                "command": "DimLvlDown",
            },
            {
                "title": "High On/Off Toggle",
                "command": "EnableHigh",
            },
            {
                "title": "To adjust the high sensitivity brightness up",
                "command": "HighLvlUp",
            },
            {
                "title": "To adjust the high sensitivity brightness down",
                "command": "HighLvlDown",
            },
            {
                "title": "To store a Dim and High memory preset level",
                "command": "MemoryStore",
            },
            {
                "title": "To recall a Dim and High memory preset level",
                "command": "MemoryRecall",
            },
            {
                "title": "To turn on the left projector",
                "command": "Display1On",
            },
            {
                "title": "To turn off the left projector",
                "command": "Display1Off",
            },
            {
                "title": "To view DVI Input on left projector",
                "command": "Display1DVI",
            },
            {
                "title": "To adjust the image brightness of the left projector to its highest level",
                "command": "Display1HighBright",
            },
            {
                "title": "To adjust the image brightness of the left projector to its lowest level",
                "command": "Display1LowBright",
            },
            {
                "title": "To turn on the right projector",
                "command": "Display2On",
            },
            {
                "title": "To turn off the right projector",
                "command": "Display2Off",
            },
            {
                "title": "To view DVI input on right projector",
                "command": "Display2DVI",
            },
            {
                "title": "To adjust the image brightness of the right projector to its highest level",
                "command": "Display2HighBright",
            },
            {
                "title": "To adjust the image brightness of the right projector to its lowest level",
                "command": "Display2LowBright",
            },
            {
                "title": "This is to set a specified time for projectors to power On/Off Toggle",
                "command": "WakeEnable",
            },
            {
                "title": "To adjust the hour parameter up for turning on the system",
                "command": "WakeHrUp",
            },
            {
                "title": "To adjust the hour parameter down for turning on the system",
                "command": "WakeHrDown",
            },
            {
                "title": "To adjust the minute parameter up for turning on the system",
                "command": "WakeMinUp",
            },
            {
                "title": "To adjust the minute parameter down for turning on the system",
                "command": "WakeMinDown",
            },
            {
                "title": "Projector power timer to set powering down of both projectors after a specified amount of time",
                "command": "SleepEnable",
            },
            {
                "title": "To adjust the hour parameter up for the projector sleep function",
                "command": "SleepHrUp",
            },
            {
                "title": "To adjust the hour parameter down for the projector sleep function",
                "command": "SleepHrDown",
            },
            {
                "title": "To adjust the minute parameter up for the projector sleep function",
                "command": "SleepMinUp",
            },
            {
                "title": "To adjust the minute parameter down for the projector sleep function",
                "command": "SleepMinDown",
            }]
