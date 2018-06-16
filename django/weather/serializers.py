from rest_framework import serializers
from weather import models


class WeatherInfoSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['name']
        model = models.WeatherInfo
        fields = [
            "id",
            "condition",
            "temperature",
            "atmosphere_pressure",
            "atmosphere_rising",
            "atmosphere_visibility",
            "atmosphere_humidity",
            "wind_direction",
            "wind_speed",
            "wind_chill",
            "created",
            ]