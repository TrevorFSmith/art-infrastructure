from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.db.models.query import Q


class LocationManager(models.Manager):
    def search(self, search_term):
        return self.filter(Q(name=search_term) | Q(gps_code=search_term) | Q(iata_code=search_term) | Q(local_code=search_term)).first()


class Location(models.Model):
    """A place like an airport used to find weather."""
    name = models.TextField(blank=False, null=False)
    airport_type = models.TextField(blank=False, null=False)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.FloatField(blank=True, null=True)
    iso_country = models.TextField(blank=True, null=True)
    iso_region = models.TextField(blank=True, null=True)
    municipality = models.TextField(blank=True, null=True)
    gps_code = models.TextField(blank=True, null=True)
    iata_code = models.TextField(blank=True, null=True)
    local_code = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = LocationManager()

    @property
    def municipality_and_country(self): return '%s, %s' % (self.municipality, self.iso_country)

    class Meta:
        ordering = ['name']

    def __unicode__(self): return self.name


class WeatherInfo(models.Model):
    '''A weather reading, probably fetched from Yahoo Weather'''
    location = models.ForeignKey(Location, blank=False)
    condition = models.TextField()
    temperature = models.FloatField()
    atmosphere_pressure = models.FloatField()
    atmosphere_rising = models.FloatField()
    atmosphere_visibility = models.FloatField()
    atmosphere_humidity = models.FloatField()
    wind_direction = models.FloatField()
    wind_speed = models.FloatField()
    wind_chill = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): return "%s" % self.id

    class Meta:
        ordering = ['-created']
