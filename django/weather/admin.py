from django.contrib import admin
from django import forms

from ai.admin import StyledModelAdmin

from models import (
    Location,
    WeatherInfo,
)

class LocationAdmin(StyledModelAdmin):
    list_display = ('id', 'name', 'iata_code', 'gps_code', 'local_code', 'created')
    search_fields = ('name', 'iata_code', 'gps_code')
admin.site.register(Location, LocationAdmin)

class WeatherInfoAdmin(StyledModelAdmin):
    pass
admin.site.register(WeatherInfo, WeatherInfoAdmin)