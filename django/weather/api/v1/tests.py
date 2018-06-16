from django.core.urlresolvers import reverse
from ai.factories import *
from ai.test_helpers import *
from rest_framework import status
from rest_framework.test import APITestCase
from weather import models as weather_models
import json


class WeatherPriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        admin_login(self)

    def test_get_200_for_privileged_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        self.assertEqual(response.status_code, 200)

    def test_get_404_for_privileged_user(self):
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': "none"}))
        self.assertEqual(response.status_code, 404)

    def test_get_weather_for_privileged_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        response_content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)

        all_keys = ["id", "condition", "temperature", "atmosphere_pressure", "atmosphere_rising", "atmosphere_visibility", 
                    "atmosphere_humidity", "wind_direction", "wind_speed", "wind_chill", "created"]
        response_all_keys = response_content.keys()
        self.assertEqual(sorted(all_keys), sorted(response_all_keys))


class WeatherUnpriviligedEndpointTestCase(APITestCase):

    def setUp(self):
        nonadmin_login(self)

    def test_get_403_for_unprivileged_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_200_for_unprivileged_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_404_for_unprivileged_user(self):
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': "none"}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})

    def test_get_weather_for_unprivileged_user(self):
        location = LocationFactory()
        response = self.client.get(reverse('weather_api:weather', kwargs={'airport_code': location.gps_code}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(json.loads(response.content), {'detail':'You do not have permission to perform this action.'})
